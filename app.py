import pandas as pd

from utils.job_parser import parse_job
from utils.ranker import rank_resumes


def main():

    print("=" * 60)
    print("        AI Resume Screening System")
    print("=" * 60)

    # Load Job
    job = parse_job("jobs/job.txt")

    # Load Resume Dataset
    df = pd.read_csv("dataset/Resume.csv")

    print("\nLoading resumes...")
    print(f"Total Resumes : {len(df)}")

    # Rank
    ranked = rank_resumes(df, job)

    print("\nTop 10 Candidates\n")

    print(ranked.head(10))

    # Save CSV
    ranked.to_csv(
        "ranked_candidates.csv",
        index=False
    )

    print("\nResults saved as ranked_candidates.csv")

    print("\nProject Completed Successfully!")


if __name__ == "__main__":
    main()