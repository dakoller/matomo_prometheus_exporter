from flask import Flask, Response
from prometheus_client import CollectorRegistry, Gauge, generate_latest
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Flask application
app = Flask(__name__)

# Prometheus registry
registry = CollectorRegistry()

# Prometheus metrics
total_visits_gauge = Gauge('matomo_visits_total', 'Total visits last hour', ['site_id', 'site_name'], registry=registry)
total_actions_gauge = Gauge('matomo_actions_total', 'Total actions last hour', ['site_id', 'site_name'], registry=registry)
unique_visitors_gauge = Gauge('matomo_unique_visitors', 'Unique visitors last hour', ['site_id', 'site_name'], registry=registry)

# Matomo API details from environment variables
MATOMO_URL = os.getenv("MATOMO_URL")
MATOMO_TOKEN = os.getenv("MATOMO_TOKEN")

# Port configuration
PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", 8000))

@app.route("/metrics")
def metrics():
    """Endpoint to expose Prometheus metrics."""

    params = {
        'token_auth': MATOMO_TOKEN,
        'format': 'json',
    }

    try:
        # Fetch sites from Matomo API
        site_response = requests.post(
            f"{MATOMO_URL}?module=API&method=SitesManager.getAllSites&format=JSON",data=params
        )
        
        if site_response.status_code == 200:
            sites = site_response.json()
            for site in sites:
                site_id = site.get("idsite")
                site_name = site.get("name")
                
                # Fetch VisitsSummary metrics for the last hour
                metrics_response = requests.post(
                    f"{MATOMO_URL}?module=API&method=VisitsSummary.get&format=JSON&idSite={site_id}&period=range&date=last1", data=params
                )
                
                if metrics_response.status_code == 200:
                    metrics = metrics_response.json()
                    total_visits = metrics.get("nb_visits", 0)
                    total_actions = metrics.get("nb_actions", 0)
                    unique_visitors = metrics.get("nb_uniq_visitors", 0)

                    # Update Prometheus metrics
                    total_visits_gauge.labels(site_id=site_id, site_name=site_name).set(total_visits)
                    total_actions_gauge.labels(site_id=site_id, site_name=site_name).set(total_actions)
                    unique_visitors_gauge.labels(site_id=site_id, site_name=site_name).set(unique_visitors)
                else:
                    print(f"Error fetching metrics for site {site_name} (ID: {site_id}): {metrics_response.text}")
        else:
            print(f"Error fetching sites: {site_response.text}")

    except Exception as e:
        print(f"Exception occurred: {e}")

    return Response(generate_latest(registry), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PROMETHEUS_PORT)
