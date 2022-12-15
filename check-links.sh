#!/bin/bash

echo Now pulling latest changes...
git pull
echo Now building site...
bundle exec jekyll build
echo Now running htmlproofer...
bundle exec htmlproofer ./_site
echo NOTE: Internal links need to be fixed. 
echo I suspect " 'a' tag is missing a reference" is an accessibility check.
echo External links can be ignored.
