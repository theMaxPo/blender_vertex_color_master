[Eng](README.md) • [Рус](README_ru.md) | [Old README](README_old.md) | [Download](https://github.com/theMaxPo/blender_vertex_color_master/releases/latest)

# Vertex Color Master for Blender

[![GitHub release](https://img.shields.io/github/v/release/theMaxPo/blender_vertex_color_master)](https://github.com/theMaxPo/blender_vertex_color_master/releases)
[![GitHub release date](https://img.shields.io/github/release-date/theMaxPo/blender_vertex_color_master)](#)
[![GitHub last commit](https://img.shields.io/github/last-commit/theMaxPo/blender_vertex_color_master)](#)
[![Static Badge](https://img.shields.io/badge/Blender-5.x-blue)](https://www.blender.org/)

An add-on for [Blender](https://www.blender.org/) that expands your workflow capabilities with Vertex Colors. Perfect for creating gradient masks for game textures and stylized model painting. [This video](https://www.youtube.com/watch?v=-OqRp9o9vQA) provides a great explanation of how Vertex Colors can be used in games.

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [License](#license)

## Features

- Linear and Radial gradients.
- Color correction operations: `HSV`, `Brightness/Contrast`, `Levels`, `Invert`, and more.
- Painting on each `RGBA` channel individually.
- and much more.

> I am 100% confident only in the functionality of the features listed above. Other legacy features from the original add-on might not work properly.

## Installation

**Requirements:** Blender 5.0 and above (should also work on earlier versions).

1. Download the latest release from the [Releases](https://github.com/theMaxPo/blender_vertex_color_master/releases) page.
2. Method 1:
   1. Drag and drop the downloaded `.zip` file into an open Blender window.
   2. Confirm the extension installation.
3. Method 2:
   1. In Blender, go to `Edit` -> `Preferences` -> `Get Extensions` (or `Add-ons`).
   2. Click the down-arrow button `\/` in the top right corner -> `Install from Disk...`.
   3. Select the downloaded `.zip` archive.
4. Ensure the `Vertex Color Master` add-on is enabled.

## Usage

1. Switch to **Vertex Paint** mode (`Ctrl+Tab+8`).
2. The add-on UI is located in the **Sidebar (N-Panel) -> VCM tab**.
3. Pressing the **`V`** key in the 3D Viewport opens the add-on's Pie menu.

## Examples

### Gradients and Operations

> Note: The .gif format distorts gradient quality, but it gives a general idea of how the tools work.

- **Linear Gradients**

<img src="README_img/1.gif" width="300" alt="Linear Gradient">

- **Radial Gradients**

<img src="README_img/3.gif" width="300" alt="Circular Gradient">

- **Complex Gradients (3+ colors)**

<img src="README_img/4.gif" width="300" alt="Linear Gradient 2+ colors">

- **HSV Color Correction**

<img src="README_img/2.gif" width="300" alt="HSV">

### Isolate Active Channel Mode

By selecting a single channel (e.g., Red `R`), you can isolate it to work exclusively in grayscale. This is incredibly useful when "packing" multiple masks into a single vertex color attribute (a common practice in game development).

- Click **Isolate Active Channel** to enter the mode.
- Use standard brushes or the add-on's tools.
- Click **Apply Changes** to bake the changes back into the main RGBA layer.

## License

This add-on is distributed under the GPL license.

Original author: [Andrew Palmer](https://github.com/andyp123).

Original repository: [Vertex Color Master](https://github.com/andyp123/vertex-color-master).
