Attribute VB_Name = "模块1"
Sub 处理BB_panel_exp()
Attribute 处理BB_panel_exp.VB_ProcData.VB_Invoke_Func = " \n14"
'
' 处理BB_panel_exp 宏
'

'
    Cells.Select
    With Selection.Font
        .Name = "Times New Roman"
        .Size = 11
        .Strikethrough = False
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleNone
        .ThemeColor = xlThemeColorLight1
        .TintAndShade = 0
        .ThemeFont = xlThemeFontNone
    End With
    With Selection.Font
        .Name = "Times New Roman"
        .Size = 12
        .Strikethrough = False
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleNone
        .ThemeColor = xlThemeColorLight1
        .TintAndShade = 0
        .ThemeFont = xlThemeFontNone
    End With
    Columns("A:G").Select
    Selection.ColumnWidth = 2.8
    Columns("C:C").Select
    Columns("C:C").EntireColumn.AutoFit
    Range("G1").Select
    ActiveSheet.Range("$A$1:$CF$56").AutoFilter Field:=7, Criteria1:="id_agent"
    ActiveSheet.Range("$A$1:$CF$56").AutoFilter Field:=7, Criteria1:="0"
    Range("F59").Select
    ActiveWorkbook.Save
End Sub
