from typing import List


class Translations:  # pragma: no cover
    __slots__ = (
        "icon",
        "short_cut",
        "scenarioString",
        "label_Language",
        "category_language",
        "option_language",
        "pushButton_SaveScenario",
        "pushButton_AddScenario",
        "pushButton_DeleteScenario",
        "pushButton_start_multiple",
        "pushButton_Cancel",
        "page_result",
        "page_settings",
        "label_Status",
        "label_File",
        "label_Calculation",
        "label_next",
        "label_previous",
        "Load",
        "SaveFigure",
        "Save",
        "label_New",
        "label_Save",
        "label_Open",
        "label_Save_As",
        "Calculation_Finished",
        "GHE_tool_imported",
        "GHE_tool_imported_start",
        "label_new_scenario",
        "new_name",
        "label_okay",
        "label_abort",
        "NoBackupFile",
        "label_close",
        "label_cancel",
        "label_CancelTitle",
        "label_LeaveScenarioText",
        "label_LeaveScenario",
        "label_StayScenario",
        "menuLanguage",
        "menuSettings",
        "menuCalculation",
        "menuFile",
        "menuScenario",
        "action_start_multiple",
        "actionNew",
        "actionSave",
        "actionOpen",
        "actionUpdate_Scenario",
        "actionAdd_Scenario",
        "actionDelete_scenario",
        "actionSave_As",
        "actionRename_scenario",
        "button_rename_scenario",
        "label_Language_Head",
        "NotCalculated",
        "NoSolution",
        "languages",
    )

    def __init__(self):
        self.languages: List[str] = ["English", "German"]
        self.icon: List[str] = ["Flag_English.svg", "Flag_German.svg"]
        self.short_cut: List[str] = ["Ctrl+Alt+E", "Ctrl+Alt+G"]
        self.scenarioString: List[str] = ["Scenario", "Szenario"]
        self.label_Language: List[str] = ["Language: ", "Sprache: "]
        self.category_language: List[str] = ["Language: ", "Sprache: "]
        self.option_language: List[str] = [
            "Language:,English,German,Dutch,Italian,French,Spanish,Galician",
            "Sprache:,English,German,Dutch,Italian,French,Spanish,Galician",
        ]
        self.pushButton_SaveScenario: List[str] = [
            "Update scenario",
            "Szenario aktualisieren",
        ]
        self.pushButton_AddScenario: List[str] = ["Add scenario", "Szenario hinzufügen"]
        self.pushButton_DeleteScenario: List[str] = [
            "Delete scenario",
            "Szenario löschen",
        ]
        self.pushButton_start_multiple: List[str] = [
            "Calculate all scenarios",
            "Berechne alle Szenarios",
        ]
        self.pushButton_Cancel: List[str] = ["Exit", "Verlassen"]
        self.page_result: List[str] = ["Results,Results", "Ergebnisse,Ergebnisse"]
        self.page_settings: List[str] = [
            "Settings,Settings",
            "Einstellungen,Einstellungen",
        ]
        self.label_Status: List[str] = ["Progress: ", "Fortschritt: "]
        self.label_File: List[str] = ["File", "Datei"]
        self.label_Calculation: List[str] = ["Calculation", "Berechnung"]
        self.label_next: List[str] = ["next", "nächstes"]
        self.label_previous: List[str] = ["previous", "vorheriges"]
        self.Load: List[str] = [
            "Choose file to load scenarios",
            "Wählen Sie die Datei zum Laden von Szenarien",
        ]
        self.SaveFigure: List[str] = [
            "Choose png location to save figure",
            "Wählen Sie einen png-Speicherort für die Abbildung",
        ]
        self.Save: List[str] = [
            "Choose file location to save scenarios",
            "Wählen Sie den Dateispeicherort zum Speichern von Szenarien",
        ]
        self.label_New: List[str] = ["New Project", "Neues Projekt"]
        self.label_Save: List[str] = ["Save Project", "Speichere Projekt"]
        self.label_Open: List[str] = ["Open Project", "Öffne Projekt"]
        self.label_Save_As: List[str] = ["Save as", "Speichere Projekt unter ..."]
        self.Calculation_Finished: List[str] = [
            "Calculation finished",
            "Berechnung fertiggestellt",
        ]
        self.GHE_tool_imported: List[str] = ["GHEtool imported", "GHEtool importiert"]
        self.GHE_tool_imported_start: List[str] = [
            "Start importing GHEtool",
            "Starte GHEtool zu importieren",
        ]
        self.label_new_scenario: List[str] = [
            "Enter new scenario name",
            "Neuer Name für das Szenario",
        ]
        self.new_name: List[str] = ["New name for ", "Neuer Name für "]
        self.label_okay: List[str] = ["Okay ", "Okay "]
        self.label_abort: List[str] = ["Abort ", "Abbruch "]
        self.NoBackupFile: List[str] = [
            "no backup fileImport",
            "Keine Sicherungsdatei gefunden",
        ]
        self.label_close: List[str] = ["Close", "Schließen"]
        self.label_cancel: List[str] = ["Cancel", "Abbrechen"]
        self.label_CancelTitle: List[str] = ["Warning", "Warnung"]
        self.label_LeaveScenarioText: List[str] = [
            "Are you sure you want to leave scenario? Any unsaved work will be lost.",
            "Bist du sicher das Szenario zu verlasen? Alle ungesicherten Änderungen gehen sonst verloren.",
        ]
        self.label_LeaveScenario: List[str] = ["Leave scenario", "Szenario verlassen"]
        self.label_StayScenario: List[str] = [
            "Stay by scenario",
            "Beim Szenario bleiben",
        ]
        self.menuLanguage: List[str] = ["Language", "Sprache"]
        self.menuSettings: List[str] = ["Settings", "Einstellungen"]
        self.menuCalculation: List[str] = ["Calculation", "Berechnung"]
        self.menuFile: List[str] = ["File", "Datei"]
        self.menuScenario: List[str] = ["Scenario", "Szenario"]
        self.action_start_multiple: List[str] = [
            "Calculate all scenarios",
            "Berechne alle Szenarios",
        ]
        self.actionNew: List[str] = ["New Project", "Neues Projekt"]
        self.actionSave: List[str] = ["Save Project", "Speichere Projekt"]
        self.actionOpen: List[str] = ["Open Project", "Öffne Projekt"]
        self.actionUpdate_Scenario: List[str] = [
            "Update scenario",
            "Szenario aktualisieren",
        ]
        self.actionAdd_Scenario: List[str] = ["Add scenario", "Szenario hinzufügen"]
        self.actionDelete_scenario: List[str] = ["Delete scenario", "Szenario löschen"]
        self.actionSave_As: List[str] = ["Save as", "Speichere Projekt unter ..."]
        self.actionRename_scenario: List[str] = [
            "Rename scenario",
            "Szenario umbenennen",
        ]
        self.button_rename_scenario: List[str] = [
            "Rename scenario",
            "Szenario umbenennen",
        ]
        self.label_Language_Head: List[str] = ["Language", "Sprache"]
        self.NotCalculated: List[str] = ["Not calculated", "Noch nicht berechnet"]
        self.NoSolution: List[str] = ["No Solution found", "Keine Lösung gefunden"]
