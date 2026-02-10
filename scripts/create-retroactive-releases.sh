#!/bin/bash
set -e

# Script to create retroactive GitHub releases for sncf-train-schedule
# This is a one-time operation to tag historical versions

echo "🏷️  Creating retroactive git tags and GitHub releases..."
echo ""

# Version-to-commit mapping from git history analysis
declare -A VERSIONS=(
    ["v0.1.0"]="51695d8"
    ["v1.1.0"]="6141543"
    ["v1.2.0"]="4236a82"
    ["v1.2.1"]="0de4ec1"
    ["v1.2.2"]="1da7fd9"
    ["v2.0.0"]="f40ea50"
    ["v2.0.1"]="a436dae"
    ["v2.1.0"]="4c5ef7e"
)

# Process versions in chronological order
for version in v0.1.0 v1.1.0 v1.2.0 v1.2.1 v1.2.2 v2.0.0 v2.0.1 v2.1.0; do
    commit="${VERSIONS[$version]}"

    echo "📦 Processing $version (commit: $commit)"

    # Check if tag already exists
    if git rev-parse "$version" >/dev/null 2>&1; then
        echo "   ⏭️  Tag $version already exists, skipping..."
        echo ""
        continue
    fi

    # Create annotated git tag
    echo "   ✓ Creating git tag..."
    git tag -a "$version" "$commit" -m "Release $version"

    # Push tag to remote
    echo "   ✓ Pushing tag to remote..."
    git push origin "$version"

    # Extract release notes from CHANGELOG.md
    echo "   ✓ Extracting release notes from CHANGELOG..."

    # Extract the version section from CHANGELOG
    # This is a simple extraction - adjust if CHANGELOG format changes
    release_notes=$(awk "/## .*$version/ {flag=1; next} /## [0-9]{4}-[0-9]{2}-[0-9]{2}/ {flag=0} flag" CHANGELOG.md)

    if [ -z "$release_notes" ]; then
        release_notes="Release $version

See CHANGELOG.md for details."
    fi

    # Check if GitHub release already exists
    if gh release view "$version" >/dev/null 2>&1; then
        echo "   ⏭️  GitHub release $version already exists, skipping..."
        echo ""
        continue
    fi

    # Create GitHub release
    echo "   ✓ Creating GitHub release..."
    echo "$release_notes" | gh release create "$version" \
        --title "$version" \
        --notes-file -

    echo "   ✅ Successfully created $version"
    echo ""
done

echo "🎉 All retroactive releases created!"
echo ""
echo "Verify with:"
echo "  git tag -l"
echo "  gh release list"
