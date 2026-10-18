# [Project Title]

> A data pipeline capstone project exploring **[topic or problem]**.

## Overview

**Problem or opportunity:** [Describe the problem this project addresses and why it matters.]

**Approach:** [Summarize the data sources, pipeline, analysis, and dashboard.]

**Key findings:** [Add the most important findings after completing the analysis.]

## Questions

List the questions that guide the project (aim for 5–10):

1. which gaming genres saw the most sales per year (aka most popular genres)? 
2. Which consoles saw the largest sales based on available data?
3. ...
4. How have video games sales changed over time?
5. which genres are more popular with each console?

## Data

Document one or two primary datasets with at least 1,000 records each, plus at least one supplementary dataset. Sources may be CSV or another suitable format, such as Parquet or an API. Avoid unstructured, unprofessional, or controversial datasets.

| Role | Dataset | Format | Approx. records | Source |
|---|---|---|---:|---|
| Primary | [Dataset name] | [CSV, Parquet, API, etc.] | [Count] | [URL] |
| Supplementary | [Dataset name] | [CSV, Parquet, API, etc.] | [Count] | [URL] |

### Dataset citations

Cite each dataset in APA style and record when it was accessed.

- [Author or organization]. ([Year]). *[Dataset title]* [Data set]. [Publisher]. [URL]. Accessed [Month Day, Year].

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

| Area | Tools |
|---|---|
| Languages and data processing | [Python, Pandas, PySpark, etc.] |
| Database and storage | [MySQL, PostgreSQL, Snowflake, etc.] |
| Orchestration | [Airflow, if used] |
| Visualization | [Dash, Power BI, etc.] |
| Other | [Additional tools] |

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