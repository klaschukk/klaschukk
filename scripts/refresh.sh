#!/usr/bin/env bash
# Refresh data/stats.json from the GitHub API (needs `gh auth login` as the profile owner,
# so private contributions are counted), then regenerate every SVG in assets/.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data
gh api graphql -f query='
query {
  viewer {
    login
    createdAt
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      totalIssueContributions
      totalPullRequestContributions
      totalRepositoriesWithContributedCommits
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date weekday contributionCount } }
      }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
      totalCount
      nodes {
        name
        isPrivate
        languages(first: 8, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}' > data/stats.json.new
mv data/stats.json.new data/stats.json
python3 scripts/gen_assets.py
