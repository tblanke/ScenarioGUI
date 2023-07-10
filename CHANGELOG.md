# ScenarioGUI's Changelog and future developments
All notable changes to this project will be documented in this file including planned future developments.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.3.0] - expected: July 2023

### Added
- Multiline text box (issue 56)
- Multiple int entry box
- Font list box
- Possibility to change figure style (issue 58) 
- Subcategory (issue 61)
- Flag in gui_structure to disable functions while loading the gui (issue 79)
- Different file extension can be saved and loaded using add_other_export_function or add_other_import_function from MainWindow class (issue 89)
- A conversation function to convert old json version styles of the gui to new ones can be added using add_other_version_import_function from MainWindow class

### Added
- Ability to deactivate button box entries (issue 46)
- Ability to deactivate aims

### Fixed
- Scenario buttons not resizing (issue 42)
- Drag scenario 2 to the place of scenario 3 do work know (issue 50)
- Scenario changing without change (issue 50)
- The scrolling in IntBoxes, FloatBoxes and ComboBoxes is disables and just working if they are selected (issue 54)
- The error messages are now completely visible (issue 59)
- Exits full screen when hovering over page buttons (issue 67)
- Flexible amount does not save (issue 69)
- Setable variable to activate the ability to set invisible elements values (issue 72)
- Problem with autosaving (issue 74)

### Changed
- list_ds in MainWindow removed and replaced by QListWidget data
- FlexOption can new be provided with default values (issue 63)
- ResultsFigure has now translatable legend texts by adding them with a commma to the current translation (example: "Label text,Y-axis,X-Axis,Line 1,Line 2") 
  (issue 65)
- Remove references to GHEtool (issue 76)
- If a value in the int Box of float box is set it is checked if the value is between the default limits and the current widget limits. If so the limits 
  are reset to the default ones and the value is set. (issue 83)
- Translation now works without the same names as the option etc.
- Redefine list_of_result_texts (issue 86)

## [0.2.2] - 2023-04-21

### Added
- The number of aims in a row can be set (issue 27)
- FilenameBox is now considering multiple file extension (issue 32)
- Float and int Box with units is implemented (issue 37)

### Fixed
- Changeable font size option is now translateable (issue 28)
- Progressbar has the correct font now
- File extension of BackUp file is now correct (issue 33)

### Changed
- ComboBox colors are set if item is highlighted
- Scenarios which are not currently running are now editable (issue 31)

## [0.2.1] - 2023-04-11

### Added
- changeable font size (issue 25)
- The number of aims in a row can be set (issue 27)

### Changed
- version number import is now relative to icons path

## [0.2.0] - 2023-04-06

### Added 
- new way of accessing the classes and functions

### Fixed
- Page button text missing

## [0.1.3] - 2023-04-03

### Added gui_config.ini will be also searched in child folders

## [0.1.2] - 2023-04-03

### Added 
- Result export button

### Fixed
- Function Button is translatable
- Aim is translatable

## [0.1.1] - 2023-03-28

### Added
- TextBox
- FlexibleAmountOption
- Configuration ini file instead of the global variables
- 3.8 compatibility
- List Box returns text value and index
- Multithreading

### Changed
- Results class and data 2 results function moved from global setting to MainWindow inputs

## [0.1.0] - 2023-03-22

### Added
- Basic functionalities
- ButtonBox
- IntBox
- Category
- Page
- FloatBox
- FileNameBox
- ResultText
- ResultFigure
- Hint
- ListBox

[0.3.0]: https://github.com/tblanke/ScenarioGUI/compare/v0.2.2...main
[0.2.2]: https://github.com/tblanke/ScenarioGUI/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/tblanke/ScenarioGUI/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/tblanke/ScenarioGUI/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/tblanke/ScenarioGUI/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/tblanke/ScenarioGUI/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/tblanke/ScenarioGUI/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/tblanke/ScenarioGUI/releases/tag/v0.1.0
