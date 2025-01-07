# This class compares the user profile to the offers previously scraped and determines
# weather these are valid offers (regarding the user CV) or not-valid ones.
#
# Valid ones are then sent to the web scraper to be filled and marked in the SQL database as valid ones to be avoided
# in future runs (invalid ones are marked as such).