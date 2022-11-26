import pandas as pd
from scipy.stats import ttest_rel
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

IND_STAGE_AVG = "Individual Staging Avg."
BULK_STAGE_AVG = "Bulk Staging Avg."
STAGE_DIFF = "Staging Difference"
OLD_PREP_AVG = "Old Prep Avg."
NEW_PREP_AVG = "New Prep Avg."
PREP_DIFF = "Prepping Difference"

def run_timed_analysis():
    # Read in the raw data from file
    raw_data = pd.read_csv('data.csv', index_col="User")

    print("Population")
    print(raw_data.to_string())

    # Construct an empty dataframe
    avg_data = pd.DataFrame()

    # Compute and add each of the averages to the data frame
    avg_data[IND_STAGE_AVG] = raw_data.T[0:3].mean().T
    avg_data[BULK_STAGE_AVG] = raw_data.T[3:6].mean().T
    avg_data[STAGE_DIFF] = avg_data[IND_STAGE_AVG] - avg_data[BULK_STAGE_AVG]
    avg_data[OLD_PREP_AVG] = raw_data.T[6:9].mean().T
    avg_data[NEW_PREP_AVG] = raw_data.T[9:12].mean().T
    avg_data[PREP_DIFF] = avg_data[OLD_PREP_AVG] - avg_data[NEW_PREP_AVG]

    print("\n\n\nIndividual Averages")
    print(avg_data.to_string())

    # Compute the mean, std, and other states for each column
    print("\n\n\nPopulation Stats")
    print(avg_data.describe().to_string())

    # Compute the paired t-tests for Individual Staging vs Bulk Staging and Old Prep Method vs New Prep Method
    print("\n\n")
    print("Paired t-test Staging: " + str(ttest_rel(avg_data[IND_STAGE_AVG], avg_data[BULK_STAGE_AVG])))
    print("Paired t-test Prepping: " + str(ttest_rel(avg_data[OLD_PREP_AVG], avg_data[NEW_PREP_AVG])))

    # Create a bar graph for staging time
    staging_plot = avg_data[[IND_STAGE_AVG, BULK_STAGE_AVG]].plot.bar(title="Average Time to Stage")
    staging_plot.set_ylabel("Seconds")

    # Create a bar graph for prepping time.
    prepping_plot = avg_data[[OLD_PREP_AVG, NEW_PREP_AVG]].plot.bar(title="Average Time to Prep")
    prepping_plot.set_ylabel("Seconds")


def run_survey_analysis():
    # Read in the raw data from file
    raw_data = pd.read_csv('survey.csv', index_col="User")

    print("Population")
    print(raw_data.to_string())
    plot = raw_data.T.plot.bar(title="Survey Responses")
    plot.set_xlabel("Question")
    plot.set_ylabel("1 = Prefer Original\n5 = Prefer Redesign")
    plot.set_ylim(bottom=1)
    plot.legend(loc="lower right", title="User")
    plot.yaxis.set_major_locator(MaxNLocator(integer=True))


if __name__ == "__main__":
    # Perform the timed data analysis
    run_timed_analysis()

    # Perform the survey data analysis
    run_survey_analysis()

    # Show the plots
    plt.show()