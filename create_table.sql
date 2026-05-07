CREATE TABLE IF NOT EXISTS job_vacancies (
    job_id BIGINT PRIMARY KEY,
    job_name TEXT NOT NULL,
    publication_date TIMESTAMP NOT NULL,
    category TEXT NOT NULL,
    levels TEXT NOT NULL,
    company_id BIGINT NOT NULL,
    location_name TEXT NOT NULL,
    company_name TEXT NOT NULL,
    landing_page TEXT NOT NULL,
    loaded_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp
)