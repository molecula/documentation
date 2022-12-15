# FeatureBase documentation

Updated documentation for Featurebase doco following alterations documented in https://molecula.atlassian.net/wiki/spaces/DOCS/pages/1007747427/Featurebase+doc+review%3A+summary+of+findings

## Theme = Minima(Jekyll default)

* Manually maintained sidebar Nav
* Page YAML differs from Post YAML

## Nav

`/_data_/navigation.yml`

* `title` - value can include upper/lowercase
* `category` - case-sensitive category name must match the folder name
* `subnav:` is for subfolders

## YAML metadata

YAML metadata affects the page title and the left nav node under the folders.

Example YAML
```
id: enterprisevscloud
title: Enterprise vs Cloud
sidebar_label: Enterprise vs Cloud
```

* id and sidebar_label affect the Nav. It's simpler to remove unless the title is too long
* NOTE: Page YAML does not affect URL.
* sidebar_label can be omitted if the nav is the same as the title

## Content filenames

Content files need to be added to `/_post` folders under the parent folders.

They take the form:
```
YYYY-MM-DD-pagename-in-url.md
```

* Posts are date-stamped
* What follows the datestamp is the page name in the URL

## External links/open in new tab

For example:
```
[Learn more about FeatureBase](https://www.featurebase.com/){:target="_blank"}
```

---

# Molecula Documentation

This repository is hosted with GitHub pages with the live site found at: https://docs.featurebase.com.

- [How Tos](#how-tos)
  * [Editing a Page](#editing-a-page)
  * [Adding a New Page](#adding-a-new-page)
  * [Adding New Images](#adding-new-images)
  * [Create a new Folder in the Navigation](#create-a-new-folder-in-the-navigation)
    + [Example Directory and Subdirectory](#example-directory-and-subdirectory)
- [Building the Documentation Locally](#building-the-documentation-locally)
- [Checking For Broken Links](#checking-for-broken-links)
- [Publishing to docs.featurebase.com](#publishing-to-docsfeaturebasecom)

## How Tos

Here is some documentation (meta documentation?) that explains how to do common actions to update the website.


### Editing a Page

The best way to edit a page is to first go to the documentation site, and at the bottom of the page find the hyperlink to "help us improve this article". From there you will be sent directly to a text editor where you can propose your changes.

**Don't worry about accidently breaking anything.** Since this site is stored as a Git repository all changes can be reverted. By design this process is to encourage quick edits by anyone in the company.

**NOTE:** Your changes require review and approval before going live.


### Adding a New Page


**[TODO]**



### Adding New Images

Images can be added to the markdown pages with:

```
![Image Title Goes Here](/img/some-image.png "Mouse Over Caption")
```

For more information on Markdown and images see: [Images | Markdown Guide](https://www.markdownguide.org/basic-syntax/#images-1).



If the image is externally hosted, then simply add the external image url and call it a day. Otherwise you'll want to host it in this repository with the following steps:

1. Set your image address as /img/{photo filename}

2. Go to https://github.com/molecula/documentation/tree/main/img

3. Find the button in the top right labeled "Add file".

4. Click "Add file" and open the dropdown. Then select "Upload files".

5. Drag and drop your image file and click "Commit changes" along with any notes what the image is used for.



### Create a new Folder in the Navigation

The directory structure for the left side navigation is defined in `_data/navigation.yml` and follows a simple hierarchical structure. Each directory is required to have the following properties:

| Key        | Required | Description                                                                                                                                        |
| ---------- |:--------:| -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `title`    | yes      | Defines a human readable format that will be displayed as the directory name.                                                                      |
| `category` | yes      | A url friendly path that will display in the address bar. <br/><br/>**NOTE:** This should not contain spaces or other non-alphanumeric characters. |
| `subnav`   | no       | Directories can be embedded within eachother by placing subfolders (and their title + categories) underneath the subnav of the parent directory.   |

#### Example Directory and Subdirectory

Assuming we want the following folder structure:

```
Hello/
  World
  FeatureBase
```

We would write the following:

```
nav:
  - title: Hello
    category: hello
    subnav:
      - title: World
        category: world

      - title: FeatureBase
        category: FeatureBase

```

**NOTE:** that nav is the top level element in the YAML file, and all directories are children of it. Also note that YAML is a space-sensitive format and each level of indent is 2 spaces.

**NOTE:** that the location of the new folder needs to be `/hello/world/_posts/`. The `_posts` directory is very important and must be added to any directory containing markdown files. The markdown files MUST be in the `_posts` directory.



## Building the Documentation Locally

For larger content edits or for changes to the theme, you'll likely need to clone the repository and edit it locally. To do so:


1. Clone the repository   
   ```
   git clone https://github.com/molecula/documentation
   ```

2. Go to the directory and install dependencies

   ```
   cd documentation
   sudo gem install bundler:2.3.9
   bundle install
   ```



3. Run the local server and visit http://localhost:4000

   ```
   bundle exec jekyll serve --watch
   ```

4. Edit files at your leisure. The site will auto-rebuild and deploy on changes so no need to repeat step 3.


## Checking For Broken Links

There are two methods to check for broken links

## Broken link checker (x86 systems only)

* html-proofer has been added to `Gemfile`
* load for the first time on a repository by running `bundle` at the command line.

Then run the broken link checker using the batch file:

```
bash check-links.sh
```

NOTE: It's important to fix internal links. External links will be reported as broken, but these need to be tested manually.

### dead_link_seeker.py (Apple, Arm systems)

Anytime you modify links, change page names, or change the nav file, please run the `dead_link_seeker.py` script. This script will crawl through all of the pages it finds off of the URL you pass, collect any URLs it sees, and call them to ensure proper health responses are returned. This should be run with python 3.6+ and uses packages that generally come installed (urllib,collections,HTMLParser), but you may have to install them conda/pip/etc. This can be run on your local build:

Run on ec2-user:
```
bundle exec jekyll serve --watch --host 0.0.0.0 &

python dead_link_seeker.py http://127.0.0.1:4000/
```

or on the website itself:

```python
python dead_link_seeker.py http://docs.featurebase.com/
```
For more detail, you may run in verbose mode by adding a `v` as a second arg.

If you add or see any pages returned that are not printed out as exceptions at the end of the output, please add them to the `false_positive` list in the script. Keep the docs healthy!



## Publishing to docs.featurebase.com
You can think of the `main` branch as being a place to stage changes and the `gh-pages` branch as the publish copy found on https://docs.featurebase.com.

When ready to go live with updates, **do not use the UI!** Instead use the following instructions below via terminal:

```bash
git clone https://github.com/molecula/documentation
cd documentation

git checkout gh-pages
git pull
git merge --ff-only origin/main
git push
```
If you don't do this then some commits seem to be lost or overwritten and that'll make authors sad :(
