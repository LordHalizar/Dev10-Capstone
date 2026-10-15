# Development Plan

Use the checkboxes to track progress. Add an estimate to each task, then record actual time spent and the completion date when checking it off (for example: `— Estimate: 2h` and, when complete, `— Actual: 1.5h; Completed: YYYY-MM-DD`). Record `—` for tasks that do not apply and explain why in the project notes or README.

**Project:** [Project title]  
**Owner(s):** [Name(s)]  
**Target presentation date:** [Date]  
**Last updated:** [Date]

## Base requirements

### 1. Project definition and planning

- [x] Create a GitHub repository for project code and deliverables.
- [x] Define the topic, problem, and audience.
- [x] Write 5–10 questions the project aims to answer.
- [x] Get peer feedback on the questions and project idea.
- [x] Discuss peer ideas for possible machine-learning applications.
- [x] Select a project-management method and track tasks, estimates, and completion dates.

### 2. Data selection and sourcing

- [x] Select one or two primary datasets, each with at least 1,000 records.
- [x] Select at least one supplementary dataset in CSV or another suitable format (for example, Parquet or an API).
- [x] Confirm that datasets are structured and appropriate for a professional project.
- [ ] Record each dataset's source, access date, format, and approximate record count.
- [ ] Add APA-format citations for all datasets.
- [ ] Check data access, usage, and sharing restrictions.

### 3. Exploration, design, and ETL

- [ ] Perform exploratory data analysis (EDA) on each dataset.
- [ ] Record raw dataset shapes, useful attributes, and data types.
- [ ] Identify missing values, inconsistencies, duplicate records, and other quality issues.
- [ ] Document where and how data will be imported and cleaned (for example, Python/Pandas or PySpark in a notebook or Airflow task).
- [ ] Define how records will be matched, deduplicated, merged, or joined across datasets.
- [ ] Design the database schema and create an ERD and DDL.
- [ ] Select and document database and any other data storage.
- [ ] Implement and document the ETL process from source through transformed data.
- [ ] Add appropriate checks to verify transformed data and joins.
- [ ] Create Airflow DAGs to orchestrate the pipeline.
- [ ] Create a dataflow diagram that identifies sources, processing, Airflow, and storage.
- [ ] Create visualizations that help explain the data and analysis.

### 4. Dashboard and presentation

- [ ] Sketch planned charts with titles and labeled axes.
- [ ] Identify the dashboard tool (Dash or Power BI) and outline the build process.
- [ ] Build and review the finalized dashboard.
- [ ] Save dashboard screenshots or exports in the repository.
- [ ] For Power BI, include a share link and PDF export.
- [ ] For Dash, include the code and screenshots.
- [ ] Create a slide deck introducing the project and its key questions.
- [ ] Include the ETL diagram and a dashboard demonstration in the presentation.
- [ ] Prepare dashboard screenshots as a contingency for the live demonstration.
- [ ] Rehearse the presentation and prepare contingencies.

### 5. Final repository and delivery

- [ ] Polish the README with the problem, questions, datasets, ETL, technologies, results, and conclusions.
- [ ] Include final ETL, database, Airflow, analysis, and dashboard code.
- [ ] Include required dashboard exports or screenshots and presentation materials.
- [ ] Write a succinct technical report covering questions, datasets, ETL, technologies, optional ML, and conclusions.
- [ ] Review the repository for completeness and ensure credentials are not committed.
- [ ] Join the Zoom presentation 15 minutes early to test audio and video.
- [ ] Present with camera and microphone off except while presenting.

## Optional requirements

### Machine learning

- [ ] Decide whether a machine-learning model is appropriate to the project questions.
- [ ] Train and reasonably tune the selected model.
- [ ] Evaluate the model with relevant metrics and/or visualizations.
- [ ] Explain model performance, limitations, and results in the README, report, and presentation.

### Snowflake

- [ ] Decide whether Snowflake is appropriate for project storage or analysis.
- [ ] Configure and document the Snowflake integration, if selected.
- [ ] Validate and describe the resulting data flow.

### Further lifecycle work

- [ ] Deploy the pipeline or model to a production-like environment, if in scope.
- [ ] Define monitoring and tracking for pipeline or model performance, if in scope.
- [ ] Identify when data, transformations, or a model should be updated.
- [ ] Use findings to propose new or improved questions.
