# Python Automation & Data Integration Tools

This repository features a collection of Python-based scripts developed to streamline technical workflows, automate data extraction via APIs, and process large datasets from video systems.

## 🚀 Key Projects & Use Cases

### 1. REST API Integration (VCA Analytics)
Developed scripts using the `requests` library to interface with VCA (Video Content Analysis) REST APIs.
*   **Functionality:** Automated extraction of real-time metadata and security events.
*   **Business Value:** Replaces manual data collection, enabling faster system auditing and more accurate reporting.

### 2. AI-Assisted Data Refinement & Formatting
Leveraged AI and Python to clean, filter, and transform raw data exports into structured formats.
*   **Functionality:** Processing "messy" data from various sources and converting it into standardized formats (JSON/CSV) for system interoperability.
*   **Value:** Demonstrates advanced problem-solving by using AI to accelerate data preparation and ensure high data quality.

### 3. Data Processing & Filtering (Encord)
Custom scripts designed to parse complex data exports from labeling and telemetry systems.
*   **Functionality:** Reads exported datasets and applies logic-based filtering to isolate specific objects or events based on technical criteria.
*   **Value:** Transforms raw logs into actionable insights for operational decision-making.

## 🛠️ Tech Stack

### Core
*   **Language:** Python 3.x
*   **Data Handling:** 
    *   `pandas`: For advanced data structure manipulation and normalization.
    *   `json` / `csv`: For parsing and saving annotation formats.
    *   `sqlite3`: Built-in engine for high-performance data querying and filtering.

### Utilities & Infrastructure
*   **API & Communication:**
    *   `requests`: For API communication and HTTP protocols.
    *   `SSE (Server-Sent Events)`: For handling real-time data streams.
*   **Media Management:**
    *   `pytube`: For video asset management and processing.
*   **UX/UI:**
    *   `tqdm`: For real-time progress bar visualization during processing.

## 📈 Impact on Implementation
These tools were built with **modularity** and **efficiency** in mind. They have successfully reduced response times in L2 support environments and simplified the integration handshake between physical security hardware and software platforms.
