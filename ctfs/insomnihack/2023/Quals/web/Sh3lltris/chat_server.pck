GDPC                                                                                  res://Root.tscn �      �       �r�.XU�Z���z�0   res://addons/godot-sqlite/bin/gdsqlite.gdnlib   P      V      �R�U.qY�ۭ�,   res://addons/godot-sqlite/bin/gdsqlite.gdns �      �       ��7�Jm�S��ңc0   res://addons/godot-sqlite/godot-sqlite.gd.remap �$      ;       �8���m�MU���th�,   res://addons/godot-sqlite/godot-sqlite.gdc  �      �       i�$�{yu4��<   res://project.binary@%      �      �U��#$�&{M��A3̊$   res://scripts/ChatServer.gd.remap   %      -       h]��;��%�Q���B.   res://scripts/ChatServer.gdc�	      ?      T5@=t��5/�����G            [gd_scene load_steps=2 format=2]

[ext_resource path="res://scripts/ChatServer.gd" type="Script" id=1]

[node name="Root" type="Node2D"]
script = ExtResource( 1 )
             [general]

singleton=false
load_once=true
symbol_prefix="godot_"
reloadable=false

[entry]

Android.armeabi-v7a="res://addons/godot-sqlite/bin/android/armeabi-v7a/libgdsqlite.so"
Android.arm64-v8a="res://addons/godot-sqlite/bin/android/arm64-v8a/libgdsqlite.so"
Android.x86="res://addons/godot-sqlite/bin/android/x86/libgdsqlite.so"
HTML5.wasm32="res://addons/godot-sqlite/bin/javascript/libgdsqlite.wasm"
OSX.64="res://addons/godot-sqlite/bin/osx/libgdsqlite.dylib"
Windows.64="res://addons/godot-sqlite/bin/win64/libgdsqlite.dll"
X11.64="res://addons/godot-sqlite/bin/x11/libgdsqlite.so"
iOS.armv7="res://addons/godot-sqlite/bin/ios/armv7/libgdsqlite.a"
iOS.arm64="res://addons/godot-sqlite/bin/ios/arm64/libgdsqlite.a"
Server="res://addons/godot-sqlite/bin/x11/libgdsqlite.so"

[dependencies]

Android.armeabi-v7a=[  ]
Android.arm64-v8a=[  ]
Android.x86=[  ]
HTML5.wasm32=[  ]
OSX.64=[  ]
Windows.64=[  ]
X11.64=[  ]
iOS.armv7=[ "res://addons/godot-sqlite/bin/ios/armv7/libgodot-cpp.ios.release.armv7.a" ]
iOS.arm64=[ "res://addons/godot-sqlite/bin/ios/arm64/libgodot-cpp.ios.release.arm64.a" ]
Server=[  ]
          [gd_resource type="NativeScript" load_steps=2 format=2]

[ext_resource path="res://addons/godot-sqlite/bin/gdsqlite.gdnlib" type="GDNativeLibrary" id=1]

[resource]
resource_name = "gdsqlite"
class_name = "SQLite"
library = ExtResource( 1 )GDSC                   �����������ض���   ����������Ӷ   ���������Ӷ�                                           
   	      
                                 YYYYYY6Y3YY0�  PQV�  -YY0�  PQV�  -Y`          GDSC   M   1   �   �     ���Ӷ���   ������Ķ   ��������������Ķ   ����   �������Ŷ���   ����������Ӷ   ������������Ķ��   ����������������ﶶ�   ���ⶶ��   ������������������Ŷ   ��Ѷ   ��������������������Ķ��   ������   ������������   ����¶��   ������¶   �����ض�   �������Ŷ���   �����׶�   �����������Ѷ���   ���ڶ���   ����������������Ŷ��   �Ҷ�   �Զ�   ���޶���   ������Զ   �������۶���   ����϶��   �������������Ŷ�   ������������������Ŷ   ��������϶��   ߶��   �����������¶���   ���Ӷ���   ��������׶��   �����Ў�   �������Զ���   �����������Ŷ���   �������Ӷ���   ������¶   ����������������Ӷ��   ն��   ��������������۶   �������Ҷ���   ��Ŷ   ������������������۶   �������۶���   ����������������Ҷ��   �������ڶ���   �������Ķ���   �������������Ӷ�   �������������������Ҷ���   ����ض��   ��Ŷ   ����Ӷ��   ��������������Ķ   ���������������Ӷ���   ��������������Ӷ   �����Ҷ�   �����Ҷ�   �����¶�   ���������¶�   �����������׶���   ���Ŷ���   �������Ķ���   ������������������Ў����   ���������������Ҷ���   ����¶��   ���Ŷ���   �������Ӷ���   ���׶���   �����������϶���   ���¶���   ��������������Ķ   ���������¶�   ���¶���   ���Ӷ���   �        binary     +   res://addons/godot-sqlite/bin/gdsqlite.gdns       user://Datastore/chat_data        client_connected      _client_connected         client_disconnected       _client_disconnected      data_received         _client_receive       peer_packet       peer_connected        multiplayer_protocol      peer_disconnected         currentRoom    @   SELECT * FROM logs where RoomName = ? ORDER BY ID DESC LIMIT 10;            Content    3   INSERT INTO Logs (RoomName, Content) VALUES (?, ?);          z         %'(),./:;<=*@&>[]+=                     9   INSERT INTO ChatRooms (RoomName, Password) VALUES (?, ?);      *   SELECT * FROM ChatRooms where RoomName = ?               RoomName   *   SELECT * FROM ChatRooms where RoomName = "        " and Password = ?;       peer   �        [         username      ]:        /                   /connect            #         /create_private          [   [SERVER] SUCCESS: private room created, access it with /login_private <roomname> <password>    H   [SERVER] ERROR: RoomName already exists or contains forbidden characters      /login_private        [SERVER] SUCCESS: logged in    *   [SERVER] Critical error, connection closed     P   [SERVER] You are connected. Join a private room or create one to start chatting!                                           #      /   	   0   
   ;      <      D      I      J      P      [      f      q      r      }      �      �      �      �      �      �      �      �      �      �      �       �   !   �   "   �   #   �   $   �   %   �   &   �   '   
  (     )     *     +   (  ,   1  -   7  .   =  /   B  0   K  1   T  2   Z  3   [  4   b  5   h  6   |  7     8   �  9   �  :   �  ;   �  <   �  =   �  >   �  ?   �  @   �  A   �  B   �  C   �  D   �  E   �  F   �  G   �  H   �  I   �  J   �  K   �  L   �  M   �  N     O     P   !  Q   $  R   (  S   0  T   6  U   ?  V   J  W   P  X   S  Y   T  Z   U  [   ^  \   n  ]   {  ^   |  _   �  `   �  a   �  b   �  c   �  d   �  e   �  f   �  g   �  h   �  i   �  j   �  k   �  l   �  m   �  n   �  o   �  p     q     r     s   +  t   9  u   B  v   I  w   L  x   i  y   s  z   v  {     |   �  }   �  ~   �     �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �     �     �     �     �      �   +  �   2  �   ?  �   K  �   W  �   ^  �   o  �   u  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   �  �   3YY;�  V�  �  T�  PQYY;�  V�  NOY;�  �  T�  Y:�  Y;�	  V�  �  PL�  MQYY;�
  V�  �  T�  PQYY:�  ?P�  QY:�  �  YY0�  PQV�  �  T�  P�  RR�  Q�  �  T�  P�  RR�  Q�  �  T�  P�  RR�	  QY�  �  T�  P�
  RR�	  Q�  �  T�  P�  RR�  RL�  MQ�  �  T�  P�  RR�  Q�  �  P�  QYY0�  P�  QV�  &�  T�  PQV�  �  T�  PQYY0�  P�  QV�  ;�  �  T�  PQ�  �  T�  �  �  �  T�  PQ�  ;�  �  L�  ML�  M�  ;�  �  �  ;�  L�  M�  �  T�  P�  R�  Q�  ;�  �  )�  �  T�   T�!  PQV�  �  �  T�   L�  �  M�  �"  P�  L�  MT�#  PQR�  Q�  �  T�$  PQ�  Y0�%  P�&  R�'  QV�  ;�  �  T�  PQ�  �  T�  �  �  �  T�  PQ�  ;�  �  �  ;�  L�&  R�'  M�  �  T�  P�  R�  Q�  �  T�$  PQYY0�(  P�&  QV�  )�)  �&  V�  &�=  P�)  Q	�  �=  P�)  Q�  �)  �  V�  .�  �  .�  �  YY0�*  P�&  R�+  QV�  ;�,  �  �  &�(  P�&  QV�  ;�  �  T�  PQ�  �  T�  �  �  �  T�  PQ�  ;�  �  �  ;�  L�&  R�+  M�  �,  �  T�  P�  R�  Q�  �  T�$  PQ�  .�,  �  Y0�-  P�&  R�+  QV�  ;�  �  T�  PQ�  �  T�  �  �  �  T�  PQ�  ;�  �  �  ;�  L�&  M�  ;�.  �  �  T�  P�  R�  Q�  &P�  T�   T�!  PQ�  QV�  �.  �  T�   L�  ML�  M�  (V�  .�  �  �  �  �.  �  �  �  L�+  M�  �  T�  P�  R�  Q�  ;�!  �  T�   T�!  PQ�  �  T�$  PQ�  .�!  YYY0�/  P�  R�0  QV�  �  L�  MN�  V�  T�1  P�  QO�  �  L�  ML�  MT�2  P�  QYY0�3  P�  R�4  �  QV�  &�  T�5  P�  QV�  �  T�6  P�  Q�  �  T�7  P�  R�   QYY0�8  P�  QV�  .�!  �  L�  ML�"  M�#  YY0�9  P�  QV�  ;�:  �;  T�  PQ�  ;�<  �  P�  P�  T�=  PQQQ�  �>  PL�  R�<  MQ�  Y0�>  P�?  QV�  ;�  �?  L�  M�  ;�<  �?  L�  M�  ;�@  �<  T�A  PQ�  &�  T�5  P�  QV�  &�@  L�  M�$  V�  ;�B  �@  T�C  P�%  R�  Q�  &�"  �  L�  MT�D  PQV�  &�@  T�C  P�%  QL�  M�&  V�  &�X  P�B  Q	�'  V�  �3  P�  R�  Q�  (V�  �  L�  ML�"  M�@  T�C  P�%  QL�  M�(  �>  P�
  T�&  PQQ�  �  L�  ML�  M�  �  (V�  &�B  L�  M�)  V�  &�X  P�B  Q	�*  V�  �3  P�  R�  Q�  (V�  ;�E  �B  L�  M�  ;�+  �B  L�'  M�  &P�*  P�E  R�+  QQV�  �"  P�+  T�#  PQR�  Q�  (V�  �"  P�,  T�#  PQR�  Q�  '�B  L�  M�-  V�  &�X  P�B  Q	�*  V�  �3  P�  R�  Q�  (V�  ;�E  �B  L�  M�  ;�+  �B  L�'  M�  ;�,  �-  P�E  R�+  Q�  &�,  �  V�  �"  P�.  T�#  PQR�  Q�  �  L�  ML�  M�E  �  �  P�  QS�  (V�  �"  P�/  T�#  PQR�  Q�  �3  P�  R�  Q�  '�"  �  L�  MT�D  PQV�  &�  L�  ML�  M�  V�  ;�F  �8  P�  QT�#  PQ�  �F  T�G  P�<  Q�  �%  P�  L�  ML�  MR�F  T�A  PQQ�  )�)  �  V�  &�)  �  �  L�)  ML�  M�  L�  ML�  MV�  �"  P�F  R�)  Q�  (V�  �"  P�0  T�#  PQR�  Q�  (V�  �3  P�  R�  QYY0�"  P�F  R�H  QV�  �  T�I  P�H  Q�  �  T�J  P�F  Q�  Y0�  P�K  QV�  �2  P�  T�  Q�  .�  T�  P�K  R�	  R�  QYY0�2  P�L  QV�  �  �L  �  )�)  �  V�  �  L�)  ML�  MT�2  P�  QY` [remap]

path="res://addons/godot-sqlite/godot-sqlite.gdc"
     [remap]

path="res://scripts/ChatServer.gdc"
   ECFG      application/config/name          Sh3lltris - Chat Server    application/run/main_scene         res://Root.tscn    editor_plugins/enabled4         %   res://addons/godot-sqlite/plugin.cfg    +   gui/common/drop_mouse_on_gui_input_disabled         )   physics/common/enable_pause_aware_picking         $   rendering/quality/driver/driver_name         GLES2   %   rendering/vram_compression/import_etc         &   rendering/vram_compression/import_etc2            