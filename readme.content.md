## Usage

### Create README configuration file
README.md generator needs a configuration file of your README, just create a file called *readme.json* in the root of your repository:

```json
{
  "PROJECT": {
    "NAME": "",
    "ICON": {
      "IMAGE": "",
      "ALT": "",
      "WIDTH": 0,
      "HEIGHT": 0
    },
    "URL": "",
    "URL_TITLE": ""
  },
  "AUTHOR": {
    "NAME": "",
    "URL": "",
    "ALT": "",
    "DATE": "",
    "SECTION": {
      "TITLE": "Author",
      "SHOW": true
    }
  },
  "DESCRIPTION": "",
  "BADGES": {
    "0": {
      "IMAGE": "",
      "HREF": "",
      "ALT": ""
    },
    "1": {
      "IMAGE": "",
      "HREF": "",
      "ALT": ""
    },
    "2": {
      "IMAGE": "",
      "HREF": "",
      "ALT": ""
    },
    ...
  },
  "CONTENT": "readme.content.md"
}
```

<details>
<summary>Example of this README</summary>

```json
{
  "PROJECT": {
    "NAME": "README.md Generator",
    "ICON": {
      "IMAGE": "icon.png",
      "ALT": "",
      "WIDTH": 200,
      "HEIGHT": 200
    },
    "URL": "",
    "URL_TITLE": ""
  },
  "AUTHOR": {
    "NAME": "Pablo Pizarro R.",
    "URL": "http://ppizarror.com",
    "ALT": "ppizarror",
    "DATE": "2017",
    "SECTION": {
      "TITLE": "Author",
      "SHOW": true
    }
  },
  "DESCRIPTION": "Generate a README.md file from a configuration file",
  "BADGES": {
    "0": {
      "IMAGE": "http://ppizarror.com/badges/author.svg",
      "HREF": "http://ppizarror.com",
      "ALT": "@ppizarror"
    },
    "1": {
      "IMAGE": "http://ppizarror.com/badges/licensemit.svg",
      "HREF": "https://opensource.org/licenses/MIT/",
      "ALT": "MIT License"
    }
  },
  "CONTENT": "readme.content.md"
}
```

</details>

## License
This project is under MIT License [https://opensource.org/licenses/MIT]