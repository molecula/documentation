# documentation



## How Tos



### Editing a Page

The best way to edit a page is to first go to the documentation site, and at the bottom of the page find the hyperlink to "help us improve this article". From there you will be sent directly to a text editor where you can propose your changes. 

**Don't worry about accidently breaking anything.** Since this site is stored as a Git repository all changes can be reverted. By design this process is to encourage quick edits by anyone in the company.

**NOTE:** Your changes require review and approval before going live. 



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
  Molecula
```

We would write the following:

```
nav:
  - title: Hello
    category: hello
    subnav:
      - title: World
        category: world

      - title: Molecula
        category: molecula 
  
```

Note that nav is the top level element in the YAML file, and all directories are children of it. Also note that YAML is a space-sensitive format and each level of indent is 2 spaces.





## Building the Documentation Locally

For larger content edits or for changes to the theme, you'll likely need to clone the repository and edit it locally. To do so:



```
git clone https://github.com/molecula/documentation
```



1. Clone the repository
   
   
   ```
   git clone https://github.com/molecula/documentation
   ```
   
   
   

2. Go to the directory and install dependencies
   
   ```
   cd documentation
   bundle install
   ```



3. Run the local server and visit http://localhost:4000
   
   ```
   bundle exec jekyll serve --watch
   ```



4. Edit files at your leisure. The site will auto-rebuild and deploy on changes so no need to repeat step 3.
