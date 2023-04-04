<!-- Filename:      README.md -->
<!-- Author:        Jonathan Delgado -->
<!-- Description:   GitHub README -->

<!-- Header -->
<h2 align="center">AutoInk(scape)</h2>
  <p align="center">
    Sublime Text plugin to quickly open Inkscape and generates figures. Heavily inspired by <a href="https://castel.dev/post/lecture-notes-2/">Gilles Castel's Inkscape workflow</a>.
    <br />
    <br />
    Status: <em>in progress</em>
    <!-- Notion Roadmap link -->
    ·<a href="https://otanan.notion.site/AutoInk-23716951ea58485c8c44e17e85ca8b27"><strong>
        Notion Roadmap »
    </strong></a>
  </p>
</div>


<!-- Project Demo -->
https://user-images.githubusercontent.com/6320907/228082814-1a3068b8-99e1-49d7-9563-5c56cd2df0bd.mov


<!-- ## Table of contents
* [Contact](#contact)
* [Acknowledgments](#acknowledgments) -->

## Description
After reading [Gilles Castel's fantastic blog posts](https://castel.dev/) on his note-taking workflow, I wanted to implement many of his ideas into my own setup with [Sublime Text]. **AutoInk** is the Sublime Text version of his [InkScape setup](https://castel.dev/post/lecture-notes-2/). It facilitates the creation of new figures, making use of existing templates, and editing figures on the fly as the document is being written. Removing the need for using the file explorer directly.

## Installation

1. Install [InkScape](https://inkscape.org/) with the command-line options. On macOS this can be done easily via [Homebrew](https://brew.sh/).
2. Copy this repository into the Sublime User folder. In macOS this would be `~/Library/Application Support/Sublime Text/Packages/User`.
3. Incorporate and modify the following lines to the preamble of a latex document to facilitate compiling directly from the `.svg` files.
```tex
\usepackage{graphicx}
% Path to figures folder
% \graphicspath{{figures}}
% Compile document with svg's through Inkscape
\usepackage{svg}
\setsvg{inkscapeexe=inkscape}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
The `.sublime-keymap` file defines the default keyboard shortcuts for running the command. For macOS the default shortcut is <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>C</kbd> to replace the current line of text for a template. Pressing <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd> opens the chooser for editing existing figures in InkScape.

In the `AutoInk.sublime-settings` file you can provide the (absolute) path to any templates. If the path is to a file, **AutoInk** will copy this without any further intervention. If the path is to a folder, then **AutoInk** will prompt each time the command is run for which template to copy (as seen in the video).

If figures folders typically have other names, then you can provide these names in the settings file. The list is ranked by priority, that is, if a figures folder is found in the same directory as a plots folder, **AutoInk** will prioritize figures by default. This can be changed by moving the plots folder higher in the list.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

Refer to the [Notion Roadmap] for future features and the state of the project.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact
Created by [Jonathan Delgado](https://jdelgado.net/).


<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Sublime Text]: https://www.sublimetext.com/
[Notion Roadmap]: https://otanan.notion.site/AutoInk-23716951ea58485c8c44e17e85ca8b27
