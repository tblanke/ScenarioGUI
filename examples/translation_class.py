from typing import List


class Translations:  # pragma: no cover
    __slots__ = (
        "icon",
        "short_cut",
        "scenarioString",
        "label_Language",
        "category_language",
        "option_language",
        "push_button_save_scenario",
        "push_button_add_scenario",
        "push_button_delete_scenario",
        "push_button_start_multiple",
        "push_button_cancel",
        "page_result",
        "page_settings",
        "label_status",
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
        "menu_language",
        "menu_settings",
        "menu_calculation",
        "menu_file",
        "menu_scenario",
        "action_start_multiple",
        "action_new",
        "action_save",
        "action_open",
        "action_update_scenario",
        "action_add_scenario",
        "action_delete_scenario",
        "action_save_as",
        "action_rename_scenario",
        "button_rename_scenario",
        "label_Language_Head",
        "NotCalculated",
        "NoSolution",
        "label_CancelText",
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
        self.push_button_save_scenario: List[str] = ["Update scenario", "Szenario aktualisieren"]
        self.push_button_add_scenario: List[str] = ["Add scenario", "Szenario hinzufügen"]
        self.push_button_delete_scenario: List[str] = ["Delete scenario", "Szenario löschen"]
        self.push_button_start_multiple: List[str] = ["Calculate all scenarios", "Berechne alle Szenarios"]
        self.push_button_cancel: List[str] = ["Exit", "Verlassen"]
        self.page_result: List[str] = ["Results,Results", "Ergebnisse,Ergebnisse"]
        self.page_settings: List[str] = ["Settings,Settings", "Einstellungen,Einstellungen"]
        self.label_status: List[str] = ["Progress: ", "Fortschritt: "]
        self.label_next: List[str] = ["next", "nächstes"]
        self.label_previous: List[str] = ["previous", "vorheriges"]
        self.Load: List[str] = ["Choose file to load scenarios", "Wählen Sie die Datei zum Laden von Szenarien"]
        self.SaveFigure: List[str] = ["Choose png location to save figure", "Wählen Sie einen png-Speicherort für die Abbildung"]
        self.Save: List[str] = ["Choose file location to save scenarios", "Wählen Sie den Dateispeicherort zum Speichern von Szenarien"]
        self.label_New: List[str] = ["New Project", "Neues Projekt"]
        self.label_Save: List[str] = ["Save Project", "Speichere Projekt"]
        self.label_Open: List[str] = ["Open Project", "Öffne Projekt"]
        self.label_Save_As: List[str] = ["Save as", "Speichere Projekt unter ..."]
        self.Calculation_Finished: List[str] = ["Calculation finished", "Berechnung fertiggestellt"]
        self.GHE_tool_imported: List[str] = ["GHEtool imported", "GHEtool importiert"]
        self.GHE_tool_imported_start: List[str] = ["Start importing GHEtool", "Starte GHEtool zu importieren"]
        self.label_new_scenario: List[str] = ["Enter new scenario name", "Neuer Name für das Szenario"]
        self.new_name: List[str] = ["New name for ", "Neuer Name für "]
        self.label_okay: List[str] = ["Okay ", "Okay "]
        self.label_abort: List[str] = ["Abort ", "Abbruch "]
        self.NoBackupFile: List[str] = ["no backup fileImport", "Keine Sicherungsdatei gefunden"]
        self.label_close: List[str] = ["Close", "Schließen"]
        self.label_cancel: List[str] = ["Cancel", "Abbrechen"]
        self.label_CancelTitle: List[str] = ["Warning", "Warnung"]
        self.label_LeaveScenarioText: List[str] = [
            "Are you sure you want to leave scenario? Any unsaved work will be lost.",
            "Bist du sicher das Szenario zu verlasen? Alle ungesicherten Änderungen gehen sonst verloren.",
        ]
        self.label_LeaveScenario: List[str] = ["Leave scenario", "Szenario verlassen"]
        self.label_StayScenario: List[str] = ["Stay by scenario", "Beim Szenario bleiben"]
        self.menu_language: List[str] = ["Language", "Sprache"]
        self.menu_settings: List[str] = ["Settings", "Einstellungen"]
        self.menu_calculation: List[str] = ["Calculation", "Berechnung"]
        self.menu_file: List[str] = ["File", "Datei"]
        self.menu_scenario: List[str] = ["Scenario", "Szenario"]
        self.action_start_multiple: List[str] = ["Calculate all scenarios", "Berechne alle Szenarios"]
        self.action_new: List[str] = ["New Project", "Neues Projekt"]
        self.action_save: List[str] = ["Save Project", "Speichere Projekt"]
        self.action_open: List[str] = ["Open Project", "Öffne Projekt"]
        self.action_update_scenario: List[str] = ["Update scenario", "Szenario aktualisieren"]
        self.action_add_scenario: List[str] = ["Add scenario", "Szenario hinzufügen"]
        self.action_delete_scenario: List[str] = ["Delete scenario", "Szenario löschen"]
        self.action_save_as: List[str] = ["Save as", "Speichere Projekt unter ..."]
        self.action_rename_scenario: List[str] = ["Rename scenario", "Szenario umbenennen"]
        self.button_rename_scenario: List[str] = ["Rename scenario", "Szenario umbenennen"]
        self.label_Language_Head: List[str] = ["Language", "Sprache"]
        self.NotCalculated: List[str] = ["Not calculated", "Noch nicht berechnet"]
        self.NoSolution: List[str] = ["No Solution found", "Keine Lösung gefunden"]
        self.label_CancelText: List[str] = [
            "Are you sure you want to quit? Any unsaved work will be lost.",
            "Bist du sicher das Programm zu schließen? Alle ungesicherten Änderungen gehen sonst verloren.",
        ]
