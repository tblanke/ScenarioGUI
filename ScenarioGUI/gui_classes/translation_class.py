

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
        "tool_imported",
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
        self.languages: list[str] = ["English", "German"]
        self.icon: list[str] = ["Flag_English.svg", "Flag_German.svg"]
        self.short_cut: list[str] = ["Ctrl+Alt+E", "Ctrl+Alt+G"]
        self.scenarioString: list[str] = ["Scenario", "Szenario"]
        self.label_Language: list[str] = ["Language: ", "Sprache: "]
        self.category_language: list[str] = ["Language: ", "Sprache: "]
        self.option_language: list[str] = [
            "Language:,English,German,Dutch,Italian,French,Spanish,Galician",
            "Sprache:,English,German,Dutch,Italian,French,Spanish,Galician",
        ]
        self.push_button_save_scenario: list[str] = ["Update scenario", "Szenario aktualisieren"]
        self.push_button_add_scenario: list[str] = ["Add scenario", "Szenario hinzufügen"]
        self.push_button_delete_scenario: list[str] = ["Delete scenario", "Szenario löschen"]
        self.push_button_start_multiple: list[str] = ["Calculate all scenarios", "Berechne alle Szenarios"]
        self.push_button_cancel: list[str] = ["Exit", "Verlassen"]
        self.page_result: list[str] = ["Results,Results", "Ergebnisse,Ergebnisse"]
        self.page_settings: list[str] = ["Settings,Settings", "Einstellungen,Einstellungen"]
        self.label_status: list[str] = ["Progress: ", "Fortschritt: "]
        self.label_next: list[str] = ["next", "nächstes"]
        self.label_previous: list[str] = ["previous", "vorheriges"]
        self.Load: list[str] = ["Choose file to load scenarios", "Wählen Sie die Datei zum Laden von Szenarien"]
        self.SaveFigure: list[str] = ["Choose png location to save figure", "Wählen Sie einen png-Speicherort für die Abbildung"]
        self.Save: list[str] = ["Choose file location to save scenarios", "Wählen Sie den Dateispeicherort zum Speichern von Szenarien"]
        self.label_New: list[str] = ["New Project", "Neues Projekt"]
        self.label_Save: list[str] = ["Save Project", "Speichere Projekt"]
        self.label_Open: list[str] = ["Open Project", "Öffne Projekt"]
        self.label_Save_As: list[str] = ["Save as", "Speichere Projekt unter ..."]
        self.Calculation_Finished: list[str] = ["Calculation finished", "Berechnung fertiggestellt"]
        self.tool_imported: list[str] = ["scenario gui imported", "scenario gui importiert"]
        self.label_new_scenario: list[str] = ["Enter new scenario name", "Neuer Name für das Szenario"]
        self.new_name: list[str] = ["New name for ", "Neuer Name für "]
        self.label_okay: list[str] = ["Okay ", "Okay "]
        self.label_abort: list[str] = ["Abort ", "Abbruch "]
        self.NoBackupFile: list[str] = ["no backup fileImport", "Keine Sicherungsdatei gefunden"]
        self.label_close: list[str] = ["Close", "Schließen"]
        self.label_cancel: list[str] = ["Cancel", "Abbrechen"]
        self.label_CancelTitle: list[str] = ["Warning", "Warnung"]
        self.label_LeaveScenarioText: list[str] = [
            "Are you sure you want to leave scenario? Any unsaved work will be lost.",
            "Bist du sicher das Szenario zu verlasen? Alle ungesicherten Änderungen gehen sonst verloren.",
        ]
        self.label_LeaveScenario: list[str] = ["Leave scenario", "Szenario verlassen"]
        self.label_StayScenario: list[str] = ["Stay by scenario", "Beim Szenario bleiben"]
        self.menu_language: list[str] = ["Language", "Sprache"]
        self.menu_settings: list[str] = ["Settings", "Einstellungen"]
        self.menu_calculation: list[str] = ["Calculation", "Berechnung"]
        self.menu_file: list[str] = ["File", "Datei"]
        self.menu_scenario: list[str] = ["Scenario", "Szenario"]
        self.action_start_multiple: list[str] = ["Calculate all scenarios", "Berechne alle Szenarios"]
        self.action_new: list[str] = ["New Project", "Neues Projekt"]
        self.action_save: list[str] = ["Save Project", "Speichere Projekt"]
        self.action_open: list[str] = ["Open Project", "Öffne Projekt"]
        self.action_update_scenario: list[str] = ["Update scenario", "Szenario aktualisieren"]
        self.action_add_scenario: list[str] = ["Add scenario", "Szenario hinzufügen"]
        self.action_delete_scenario: list[str] = ["Delete scenario", "Szenario löschen"]
        self.action_save_as: list[str] = ["Save as", "Speichere Projekt unter ..."]
        self.action_rename_scenario: list[str] = ["Rename scenario", "Szenario umbenennen"]
        self.button_rename_scenario: list[str] = ["Rename scenario", "Szenario umbenennen"]
        self.label_Language_Head: list[str] = ["Language", "Sprache"]
        self.NotCalculated: list[str] = ["Not calculated", "Noch nicht berechnet"]
        self.NoSolution: list[str] = ["No Solution found", "Keine Lösung gefunden"]
        self.label_CancelText: list[str] = [
            "Are you sure you want to quit? Any unsaved work will be lost.",
            "Bist du sicher das Programm zu schließen? Alle ungesicherten Änderungen gehen sonst verloren.",
        ]
