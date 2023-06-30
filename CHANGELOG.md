# ScenarioGUI's Changelog and future developments
All notable changes to this project will be documented in this file including planned future developments.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.3.0] - expected: june 2023

### Added
- Multiline text box (issue 56)
- Multiple int entry box
- Font list box
- Possibility to change figure style (issue 58) 
- Subcategory (issue 61)

### Fixed
- Scenario buttons not resizing (issue 42)
- Drag scenario 2 to the place of scenario 3 do work know (issue 50)
- Scenario changing without change (issue 50)
- The scrolling in IntBoxes, FloatBoxes and ComboBoxes is disables and just working if they are selected (issue 54)
- The error messages are now completely visible (issue 59)
- Exits full screen when hovering over page buttons (issue 67)

### Changed
- list_ds in MainWindow removed and replaced by QListWidget data
- FlexOption can new be provided with default values (issue 63)

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
