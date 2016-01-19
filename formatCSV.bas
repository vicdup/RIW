Attribute VB_Name = "Module1"
Sub format()
Attribute format.VB_ProcData.VB_Invoke_Func = " \n14"
'
' format Macro
'

'
    Range("A1:CW64").Select
    Selection.Copy
    Sheets.Add After:=ActiveSheet
    Selection.PasteSpecial Paste:=xlPasteAll, Operation:=xlNone, SkipBlanks:= _
        False, Transpose:=True
    Application.CutCopyMode = False
    Selection.FormatConditions.Add Type:=xlTextString, String:="p", _
        TextOperator:=xlContains
    Selection.FormatConditions(Selection.FormatConditions.Count).SetFirstPriority
    With Selection.FormatConditions(1).Interior
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorAccent6
        .TintAndShade = 0.399945066682943
    End With
    Selection.FormatConditions(1).StopIfTrue = False
    ActiveSheet.ListObjects.Add(xlSrcRange, Range("$A$1:$BL$101"), , xlYes).Name = _
        "Table1"
    Range("Table1[#All]").Select
    ActiveSheet.ListObjects("Table1").TableStyle = "TableStyleLight16"
    ActiveSheet.ListObjects("Table1").ShowTableStyleRowStripes = False
    ActiveSheet.ListObjects("Table1").ShowTableStyleColumnStripes = True
    Range("J5").Select
End Sub
