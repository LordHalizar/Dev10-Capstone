# Dev10 Capstone Project by Alexander Crosby

> A data pipeline capstone project exploring **video game sales from 1980 to 2015**.

## Overview

**Problems:** 
1. Analyzing, processing, and loading data to local database.
2. Creating dashboard visualizations with data from database.
3. Data upload from local database to cloud server equivalent database.
4. Containerize all processes to allow automated application of processes above.

**Approach:**
1. Adaptive ET (extract & transform) for filtering & shaping data, with TL (transform & load) for data refinement and eventual loading to local database.
2. SQLAlchemy engine to allow SQL calls to local database & callbacks system & plotly to shape and visualize data into tables & graphs.
3. SQLExecuteQueryOperator to create assignment tasks and execute containerized snowflake schema followed by reusable/generalized sql query function to grab necessary columns from individual tables. Function then called several times for all necessary database tables.
4. Docker file structure implemented with dedicated folders for nearly all functionalities. Individual functions then encapsulated and called as DAGs through Airflow.

**Key findings:** [Add the most important findings after completing the analysis.]

## Questions

List the questions that guide the project (aim for 5–10):

1. How has the popularity of video games changed over time? 
2. Which genres sold better in which regions?
3. Which consoles sold better in which regions?
4. How do gaming consoles drive video game sales?
5. When did publishers see their greatest sales?

## Data


| Role | Dataset | Format | Approx. records | Source |
|---|---|---|---:|---|
| Primary | [Dataset name] | [CSV, Parquet, API, etc.] | [Count] | [URL] |
| Supplementary | [Dataset name] | [CSV, Parquet, API, etc.] | [Count] | [URL] |

### Dataset citations

#### Video Game Sales with Ratings
Rush4ratio. (n.d.). Video game sales with ratings [Data set]. Kaggle. https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings/data
*Source note: Dataset scraped from Metacritic.*

#### Video Game Sales
Gregorut. (n.d.). Video game sales [Data set]. Kaggle. https://www.kaggle.com/datasets/gregorut/videogamesales
*Source note: Dataset scraped from VGChartz.*

## Data pipeline

Describe how data moves through the project. Replace the outline with a diagram when the design is established.

```text
[Data sources] -> [Ingestion] -> [Cleaning and transformation] -> [Database or storage]
                                                                  -> [Analysis] -> [Dashboard]
```

- **Ingestion:** [How each source is obtained and loaded.]
- **Cleaning and transformation:** [Tools, location, quality checks, and key changes.]
- **Joining and merging:** [How datasets are matched; explain how duplicate or equivalent records are handled.]
- **Storage and schema:** [Database, tables, data types, and link to the ERD or DDL.]
- **Orchestration:** [Airflow DAGs and their schedules or dependencies, if applicable.]

## Dashboard and presentation

- **Dashboard:** [Dash or Power BI; add a link or instructions to open it.]
- **Exports or screenshots:** [Link to PDF, images, or dashboard captures in this repository.]
- **Presentation:** [Link to the slide deck.]

The presentation should introduce the project and its key questions, explain the ETL flow, demonstrate the dashboard (with screenshots as a backup), summarize any optional machine-learning results, and share conclusions.

## Technologies

|              Area             |               Tools               |
|---                         ---|---                             ---|
|Languages and data processing  |[Python, Pandas, PySpark, etc.]    |
|Database and storage           |[PostgreSQL, Snowflake, SQLAlchemy]|
|Orchestration                  |[Airflow, Docker]                  |
|Visualization                  |[Dash, Canvas, Plotly]             |
|Other                          |[Additional tools]                 |

## Repository contents

Add or update this list to match the actual repository structure.

- Data acquisition, cleaning, and ETL code
- Database schema, DDL, and/or ERD
- Airflow DAGs and pipeline documentation
- Analysis and visualization sketches
- Dashboard code, exports, or screenshots
- Presentation materials and technical report

## Setup and usage

Document the steps needed to reproduce the project. Replace these placeholders with the commands and configuration required by the implementation.

### Prerequisites

- [Language/runtime and version]
- [Database or other required services]
- [Any other prerequisites]

### Install and run

```text
[Installation commands]
[Configuration instructions; do not commit credentials]
[ETL or orchestration commands]
[Dashboard launch commands]
```

Explain where to obtain the data and how to configure access. Do not commit credentials or restricted datasets; document any access limitations and provide download instructions where permitted.

## Results and conclusions

[Summarize the analysis, visualizations, limitations, and conclusions. Explain which questions were answered and identify useful follow-up questions.]

### Machine learning (optional)

[If used, describe the goal, model, training and tuning approach, evaluation metrics, and results. Otherwise, state that machine learning was out of scope.]

## Development progress

Track implementation tasks in [DevelopmentPlan.md](./DevelopmentPlan.md).

## Acknowledgments

[Credit collaborators, instructors, and data providers as appropriate.]

Verma, P. (2025, November 11). Video games sales. Kaggledatasets. https://www.kaggle.com/datasets/lamskdna/video-games-sales

Video game sales with ratings. (n.d.). Www.Kaggle.Com. Retrieved October 17, 2026, from https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings/data

Free sample dataset download - video game sales - maven analytics | build data skills, faster. (2024). Mavenanalytics.Io. https://mavenanalytics.io/data-playground/video-game-sales