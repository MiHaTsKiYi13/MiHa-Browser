/*
This script works on Windows 10 with 64 and 32 bit AHK
and on Windows 7 with 64 bit AHK (but not 32 bit), if DWM is turned on (Aero theme).

Use Shift + LButton hotkey to select a new area on the screen, where colors will be inverted
Use Shift + RButton hotkey to delete the previously selected area
Use F9 hotkey to hide/show selected areas and turn off/on Shift + LButton and Shift + RButton hotkeys
*/

/*
; try uncommenting this block, if the scrit doesn't work with some needed windows

If !RegExMatch(DllCall("GetCommandLine", "Str"), " /restart(?!\S)") {
   If (A_PtrSize = 8)
      RunWait "C:\Program Files\AutoHotkey\AutoHotkeyU64_UIA.exe" /restart "%A_ScriptFullPath%"
   Else If A_IsUnicode
      RunWait "C:\Program Files\AutoHotkey\AutoHotkeyU32_UIA.exe" /restart "%A_ScriptFullPath%"
   Else
      RunWait "C:\Program Files\AutoHotkey\AutoHotkeyA32_UIA.exe" /restart "%A_ScriptFullPath%"
}
*/

#NoEnv
#UseHook
SetWinDelay 0
SetBatchLines -1
toggle := true
DllCall("Dwmapi\DwmIsCompositionEnabled", "UIntP", bool)
if !bool {
   MsgBox, 64, DWM, DWM is turned off, this script will not work. Choose the Aero theme and launch the script again!
   ExitApp
}

F9::
   toggle := !toggle
   Magnifier.ToggleShow()
Return

#If toggle
+LButton::
SelectNewArea() {
   Magnifier.stop := true
   area := SelectedArea.Start(0x82FFC800)
   if !(area.w > 10 && area.h > 10)
      Return
   timer := ObjBindMethod(Magnifier, "CreateMagnifier", area)
   SetTimer, % timer, -10
}

+RButton::
DeleteMagnifierUnderMouse() {
   DllCall("GetCursorPos", "Int64P", POINT)
   for k, gui in Magnifier.GUIs {
      if DllCall("PtInRect", "Ptr", gui.area.pRect, "Int64", POINT) {
         Gui, % gui.hGui . ":Destroy"
         break
      }
   }
}

class SelectedArea
{
   Start(colorARGB) {
      area := {x: 0, y: 0, w: 0, h: 0}
      this.ReplaceSystemCursors("IDC_CROSS")
      this.Select(area, colorARGB)
      this.ReplaceSystemCursors("")
      Return area
   }
   
   Select(area, colorARGB) {
      this.hGui := this.CreateSelectionGui(colorARGB)
      Hook := new this.WindowsHook(WH_MOUSE_LL := 14, ObjBindMethod(this, "LowLevelMouseProc"))
      KeyWait, LButton
      Hook := ""
      WinGetPos, x, y, w, h
      Gui, Destroy
      for k in area
         area[k] := %k%
   }
   
   CreateSelectionGui(colorARGB) {
      Gui, New, +hwndhGui +Alwaysontop -Caption +LastFound +ToolWindow +E0x20 -DPIScale
      WinSet, Transparent, % colorARGB >> 24
      Gui, Color, % Format("{:X}", colorARGB & 0xFFFFFF)
      Return hGui
   }
   
   ReplaceSystemCursors(IDC = "")
   {
      static IMAGE_CURSOR := 2, SPI_SETCURSORS := 0x57
           , SysCursors := { IDC_APPSTARTING: 32650
                           , IDC_ARROW      : 32512
                           , IDC_CROSS      : 32515
                           , IDC_HAND       : 32649
                           , IDC_HELP       : 32651
                           , IDC_IBEAM      : 32513
                           , IDC_NO         : 32648
                           , IDC_SIZEALL    : 32646
                           , IDC_SIZENESW   : 32643
                           , IDC_SIZENWSE   : 32642
                           , IDC_SIZEWE     : 32644
                           , IDC_SIZENS     : 32645 
                           , IDC_UPARROW    : 32516
                           , IDC_WAIT       : 32514 }
      if !IDC
         DllCall("SystemParametersInfo", "UInt", SPI_SETCURSORS, "UInt", 0, "UInt", 0, "UInt", 0)
      else {
         hCursor := DllCall("LoadCursor", "Ptr", 0, "UInt", SysCursors[IDC], "Ptr")
         for k, v in SysCursors {
            hCopy := DllCall("CopyImage", "Ptr", hCursor, "UInt", IMAGE_CURSOR, "Int", 0, "Int", 0, "UInt", 0, "Ptr")
            DllCall("SetSystemCursor", "Ptr", hCopy, "UInt", v)
         }
      }
   }
   
   LowLevelMouseProc(nCode, wParam, lParam) {
      static WM_MOUSEMOVE := 0x200, WM_LBUTTONUP := 0x202
           , coords := [], startMouseX, startMouseY, timer
      if !timer
         timer := ObjBindMethod(this, "LowLevelMouseProc", "timer", "", "")
      if (nCode = "timer") {
         while coords[1] {
            point := coords.RemoveAt(1)
            mouseX := point[1], mouseY := point[2]
            x := startMouseX < mouseX ? startMouseX : mouseX
            y := startMouseY < mouseY ? startMouseY : mouseY
            w := Abs(mouseX - startMouseX)
            h := Abs(mouseY - startMouseY)
            try Gui, % this.hGui . ":Show", x%x% y%y% w%w% h%h% NA
         }
      }
      else {
         if (wParam = WM_LBUTTONUP)
            startMouseX := startMouseY := ""
         if (wParam = WM_MOUSEMOVE) {
            mouseX := NumGet(lParam + 0, "Int")
            mouseY := NumGet(lParam + 4, "Int")
            if (startMouseX = "") {
               startMouseX := mouseX
               startMouseY := mouseY
            }
            coords.Push([mouseX, mouseY])
            SetTimer, % timer, -10
         }
         Return DllCall("CallNextHookEx", "Ptr", 0, "Int", nCode, "UInt", wParam, "Ptr", lParam)
      }
   }

   class WindowsHook {
      __New(type, callBack, isGlobal := true) {
         this.BoundCallback := new this.BoundFuncCallback(callBack, 3, "Fast")
         this.hHook := DllCall("SetWindowsHookEx", "Int", type, "Ptr", this.BoundCallback.addr
                                                 , "Ptr", !isGlobal ? 0 : DllCall("GetModuleHandle", "UInt", 0, "Ptr")
                                                 , "UInt", isGlobal ? 0 : DllCall("GetCurrentThreadId"), "Ptr")
      }
      __Delete() {
         DllCall("UnhookWindowsHookEx", "Ptr", this.hHook)
         this.BoundCallback := ""
      }

      class BoundFuncCallback
      {
         __New(BoundFuncObj, paramCount, options := "") {
            this.pInfo := Object( {BoundObj: BoundFuncObj, paramCount: paramCount} )
            this.addr := RegisterCallback(this.__Class . "._Callback", options, paramCount, this.pInfo)
         }
         __Delete() {
            ObjRelease(this.pInfo)
            DllCall("GlobalFree", "Ptr", this.addr, "Ptr")
         }
         _Callback(Params*) {
            Info := Object(A_EventInfo), Args := []
            Loop % Info.paramCount
               Args.Push( NumGet(Params + A_PtrSize*(A_Index - 2)) )
            Return Info.BoundObj.Call(Args*)
         }
      }
   }
}

class Magnifier
{
   static GUIs := []
   CreateMagnifier(area) {
      static onExitSet := false
      this.show := true
      (!this.onDestroy && this.onDestroy := ObjBindMethod(this, "WM_DESTROY"))
      if !this.GUIs.Count() {
         this.MagInitialize()
         OnMessage(0x0002, this.onDestroy)
      }
      (!onExitSet && OnExit( ObjBindMethod(this, "Clear"), onExitSet := true ))
      Gui := new this.MagGui(area)
      this.GUIs[Gui.hGui] := Gui
      this.stop := false
      this.MainLoop()
   }
   
   MagInitialize() {
      if !this.hLib := DllCall("LoadLibrary", "str", "Magnification.dll") {
         MsgBox, 16, Error, Failed to load Magnification.dll
         Return
      }
      Return DllCall("Magnification\MagInitialize")
   }
   
   Clear() {
      if !this.hLib
         Return
      DllCall("Magnification\MagUninitialize")
      DllCall("FreeLibrary", "Ptr", this.hLib)
      this.hLib := ""
      OnMessage(0x0002, this.onDestroy, 0)
   }
   
   MainLoop() {
      while !this.stop {
         for k, gui in this.GUIs
            this.Update(gui)
      }
   }
   
   Update(gui) {
      area := gui.area
      params := A_PtrSize = 8 ? ["Ptr", area.pRect] : ["Int", area.x, "Int", area.y, "Int", area.r, "Int", area.b]
      DllCall("Magnification\MagSetWindowSource", "Ptr", gui.hMag, params*)
      if !DllCall("IsWindowVisible", "Ptr", gui.hGui)
         try Gui, % gui.hGui . ":Show", % "NA x" . area.x . " y" . area.y . " w" . area.w . " h" . area.h
   }
   
   ToggleShow(mode := "toggle") {
      static areas := []
      Switch mode {
         case "toggle":
            this.show := !this.show
            if (this.show && areas.Count()) {
               timer := ObjBindMethod(this, "ToggleShow", "timer")
               SetTimer, % timer, 100
            }
            if !this.show {
               this.stop := true
               Sleep 100
               for k, gui in this.GUIs
                  areas.Push(gui.area)
               this.GUIs := []
               this.Clear()
            }
         case "timer":
            timer := ObjBindMethod(this, "CreateMagnifier", areas.Pop())
            SetTimer, % timer, -10
            if !areas.Count()
               SetTimer,, Delete
      }
   }

   WM_DESTROY() {
      if !this.GUIs.HasKey(A_Gui)
         Return
      this.GUIs.Delete(A_Gui)
      if !this.GUIs.Count() {
         this.stop := true
         this.Clear()
      }
   }
   
   class MagGui
   {
      __New(area) {
         this.area := area
         area.r := area.x + area.w
         area.b := area.y + area.h
         this.area.SetCapacity("RECT", 16)
         this.area.pRect := this.area.GetAddress("RECT")
         for k, v in ["x", "y", "r", "b"]
            NumPut(area[v], this.area.pRect + 4*(k - 1), "UInt")
         this.CreateGui()
      }
      
      __Delete() {
         try Gui, % this.hGui . ":Destroy"
      }
      
      CreateGui() {
         static MS_INVERTCOLORS := 0x0004
              , exStyles := (WS_EX_TRANSPARENT := 0x00000020)
                          | (WS_EX_COMPOSITED  := 0x02000000)
                          | (WS_EX_LAYERED     := 0x00080000)
         
         area := this.area         
         Gui, New, +hwndhGui -Caption -DPIScale +AlwaysOnTop +Owner +E%exStyles%
         Gui, Margin, 0, 0
         Gui, Add, Custom, % "hwndhMag ClassMagnifier +" . MS_INVERTCOLORS . " w" . area.w . " h" . area.h
         this.hGui := hGui, this.hMag := hMag
      }
   }
}