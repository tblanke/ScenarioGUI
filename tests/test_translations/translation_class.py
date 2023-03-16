from typing import List


class Translations:  # pragma: no cover
    __slots__ = (
        "action_add_scenario",
        "action_delete_scenario",
        "action_new",
        "action_open",
        "action_rename_scenario",
        "action_save",
        "action_save_as",
        "action_start_multiple",
        "action_update_scenario",
        "button_rename_scenario",
        "Calculation_Finished",
        "category_language",
        "icon",
        "label_abort",
        "label_cancel",
        "label_CancelText",
        "label_CancelTitle",
        "label_close",
        "label_Language",
        "label_Language_Head",
        "label_LeaveScenario",
        "label_LeaveScenarioText",
        "label_New",
        "label_new_scenario",
        "label_next",
        "label_okay",
        "label_Open",
        "label_previous",
        "label_Save",
        "label_Save_As",
        "label_status",
        "label_StayScenario",
        "Load",
        "menu_calculation",
        "menu_file",
        "menu_language",
        "menu_scenario",
        "menu_settings",
        "new_name",
        "NoBackupFile",
        "NoSolution",
        "NotCalculated",
        "option_language",
        "page_result",
        "page_settings",
        "push_button_add_scenario",
        "push_button_cancel",
        "push_button_delete_scenario",
        "push_button_save_scenario",
        "push_button_start_multiple",
        "Save",
        "SaveFigure",
        "scenarioString",
        "short_cut",
        "tool_imported",
        "choose_load",
        "option_toggle_buttons",
        "languages",
    )

    def __init__(self):
        self.languages: List[str] = ["English", "German"]
        self.action_add_scenario: list[str] = ["Add scenario", "Szenario hinzufügen"]
        self.action_delete_scenario: list[str] = ["Delete scenario", "Szenario löschen"]
        self.action_new: list[str] = ["New Project", "Neues Projekt"]
        self.action_open: list[str] = ["Open Project", "Öffne Projekt"]
        self.action_rename_scenario: list[str] = ["Rename scenario", "Szenario umbenennen"]
        self.action_save: list[str] = ["Save Project", "Speichere Projekt"]
        self.action_save_as: list[str] = ["Save as", "Speichere Projekt unter ..."]
        self.action_start_multiple: list[str] = ["Calculate all scenarios", "Berechne alle Szenarios"]
        self.action_update_scenario: list[str] = ["Update scenario", "Szenario aktualisieren"]
        self.button_rename_scenario: list[str] = ["Rename scenario", "Szenario umbenennen"]
        self.Calculation_Finished: list[str] = ["Calculation finished", "Berechnung fertiggestellt"]
        self.category_language: list[str] = ["Language: ", "Sprache: "]
        self.icon: list[str] = ["Flag_English.svg", "Flag_German.svg"]
        self.label_abort: list[str] = ["Abort ", "Abbruch "]
        self.label_cancel: list[str] = ["Cancel", "Abbrechen"]
        self.label_CancelText: list[str] = [
            "Are you sure you want to quit? Any unsaved work will be lost.",
            "Bist du sicher das Programm zu schließen? Alle ungesicherten Änderungen gehen sonst verloren.",
        ]
        self.label_CancelTitle: list[str] = ["Warning", "Warnung"]
        self.label_close: list[str] = ["Close", "Schließen"]
        self.label_Language: list[str] = ["Language: ", "Sprache: "]
        self.label_Language_Head: list[str] = ["Language", "Sprache"]
        self.label_LeaveScenario: list[str] = ["Leave scenario", "Szenario verlassen"]
        self.label_LeaveScenarioText: list[str] = [
            "Are you sure you want to leave scenario? Any unsaved work will be lost.",
            "Bist du sicher das Szenario zu verlasen? Alle ungesicherten Änderungen gehen sonst verloren.",
        ]
        self.label_New: list[str] = ["New Project", "Neues Projekt"]
        self.label_new_scenario: list[str] = ["Enter new scenario name", "Neuer Name für das Szenario"]
        self.label_next: list[str] = ["next", "nächstes"]
        self.label_okay: list[str] = ["Okay ", "Okay "]
        self.label_Open: list[str] = ["Open Project", "Öffne Projekt"]
        self.label_previous: list[str] = ["previous", "vorheriges"]
        self.label_Save: list[str] = ["Save Project", "Speichere Projekt"]
        self.label_Save_As: list[str] = ["Save as", "Speichere Projekt unter ..."]
        self.label_status: list[str] = ["Progress: ", "Fortschritt: "]
        self.label_StayScenario: list[str] = ["Stay by scenario", "Beim Szenario bleiben"]
        self.Load: list[str] = ["Choose file to load scenarios", "Wählen Sie die Datei zum Laden von Szenarien"]
        self.menu_calculation: list[str] = ["Calculation", "Berechnung"]
        self.menu_file: list[str] = ["File", "Datei"]
        self.menu_language: list[str] = ["Language", "Sprache"]
        self.menu_scenario: list[str] = ["Scenario", "Szenario"]
        self.menu_settings: list[str] = ["Settings", "Einstellungen"]
        self.new_name: list[str] = ["New name for ", "Neuer Name für "]
        self.NoBackupFile: list[str] = ["no backup fileImport", "Keine Sicherungsdatei gefunden"]
        self.NoSolution: list[str] = ["No Solution found", "Keine Lösung gefunden"]
        self.NotCalculated: list[str] = ["Not calculated", "Noch nicht berechnet"]
        self.option_language: list[str] = [
            "Language:,English,German,Dutch,Italian,French,Spanish,Galician",
            "Sprache:,English,German,Dutch,Italian,French,Spanish,Galician",
        ]
        self.page_result: list[str] = ["Results,Results", "Ergebnisse,Ergebnisse"]
        self.page_settings: list[str] = ["Settings,Settings", "Einstellungen,Einstellungen"]
        self.push_button_add_scenario: list[str] = ["Add scenario", "Szenario hinzufügen"]
        self.push_button_cancel: list[str] = ["Exit", "Verlassen"]
        self.push_button_delete_scenario: list[str] = ["Delete scenario", "Szenario löschen"]
        self.push_button_save_scenario: list[str] = ["Update scenario", "Szenario aktualisieren"]
        self.push_button_start_multiple: list[str] = ["Calculate all scenarios", "Berechne alle Szenarios"]
        self.Save: list[str] = ["Choose file location to save scenarios", "Wählen Sie den Dateispeicherort zum Speichern von Szenarien"]
        self.SaveFigure: list[str] = ["Choose png location to save figure", "Wählen Sie einen png-Speicherort für die Abbildung"]
        self.scenarioString: list[str] = ["Scenario", "Szenario"]
        self.short_cut: list[str] = ["Ctrl+Alt+E", "Ctrl+Alt+G"]
        self.tool_imported: list[str] = ["scenario gui imported", "scenario gui importiert"]
        self.choose_load: list[str] = ["Choose file to load scenarios", "Wählen Sie Datei zum Laden von Szenarien"]
        self.option_toggle_buttons: list[str] = ["Use toggle buttons?:, no , yes ", "Umschalterbutton?:, Nein , Ja "]