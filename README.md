# Matomo VisitsSummary Prometheus Exporter

## Overview
This script collects VisitsSummary metrics from a self-hosted Matomo instance and exposes them in Prometheus format. It retrieves the metrics for the last hour for each site managed in the Matomo instance and includes the site name in the Prometheus output.

## Features
- Exposes the following metrics:
  - `matomo_visits_total`: Total visits in the last hour.
  - `matomo_actions_total`: Total actions in the last hour.
  - `matomo_unique_visitors`: Unique visitors in the last hour.
- Includes `site_id` and `site_name` as labels in the metrics.
- Configurable Prometheus port via environment variables.

## Prerequisites
- Python 3.7+
- Access to a self-hosted Matomo instance with an API token.
- Prometheus installed and configured.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/matomo-prometheus-exporter.git
   cd matomo-prometheus-exporter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following content:
   ```env
   MATOMO_URL=https://your-matomo-instance/index.php
   MATOMO_TOKEN=your_matomo_api_token
   PROMETHEUS_PORT=8000  # Optional, default is 8000
   ```

## Usage
1. Run the script:
   ```bash
   python matomo_visits_prometheus.py
   ```

2. Access the metrics endpoint at:
   ```
   http://<host>:<PROMETHEUS_PORT>/metrics
   ```

## Prometheus Integration
1. Add the following scrape configuration to your Prometheus configuration:
   ```yaml
   scrape_configs:
     - job_name: 'matomo'
       static_configs:
         - targets: ['<host>:<PROMETHEUS_PORT>']
   ```

2. Reload your Prometheus configuration to apply the changes.

## Example Output
Example metrics exposed by the script:
```
# HELP matomo_visits_total Total visits last hour
# TYPE matomo_visits_total gauge
matomo_visits_total{site_id="1",site_name="My Site"} 100

# HELP matomo_actions_total Total actions last hour
# TYPE matomo_actions_total gauge
matomo_actions_total{site_id="1",site_name="My Site"} 250

# HELP matomo_unique_visitors Unique visitors last hour
# TYPE matomo_unique_visitors gauge
matomo_unique_visitors{site_id="1",site_name="My Site"} 80
```

## Notes
- Ensure that the Matomo API token has sufficient permissions to access site and summary data.
- Protect the metrics endpoint and API token to avoid unauthorized access.

## Troubleshooting
1. If no metrics appear:
   - Check the `.env` file for correct values.
   - Verify that the Matomo API is accessible.

2. For connection issues:
   - Ensure the host running the script is accessible to Prometheus.
   - Check for firewall or network restrictions.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

