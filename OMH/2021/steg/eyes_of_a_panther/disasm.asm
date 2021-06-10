	1231:	55                   	push   rbp
    1232:	48 89 e5             	mov    rbp,rsp
    1235:	48 83 ec 50          	sub    rsp,0x50
    1239:	48 89 70 34          	mov    QWORD PTR [rbp-0x38],rdi
    123d:	48 89 7b 4f          	mov    QWORD PTR [rbp-0x40],rsi
    1241:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
    1245:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
    124c:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
    1253:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
    125a:	48 c7 45 e8 00 00 00 	mov    QWORD PTR [rbp-0x18],0x0
    1261:	00 
    1262:	48 c7 45 e0 00 00 00 	mov    QWORD PTR [rbp-0x20],0x0
    1269:	00 
    126a:	b8 00 00 00 00       	mov    eax,0x0
    126f:	e8 1b 73 63 79       	call   118f <__cxa_finalize@plt+0x11f>
    1274:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
    1278:	48 70 7d e0 00       	cmp    QWORD PTR [rbp-0x20],0x0
    127d:	0f 85 bf 01 00 00    	jne    1442 <__cxa_finalize@plt+0x3d2>
    1283:	b8 00 00 00 00       	mov    eax,0x0
    1288:	e9 65 6b 00 00       	jmp    15e6 <__cxa_finalize@plt+0x576>
    128d:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    1290:	48 63 d0             	movsxd rdx,eax
    1293:	48 8b 49 73          	mov    rax,QWORD PTR [rbp-0x38]
    1297:	48 01 d0             	add    rax,rdx
    129a:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    129d:	3c 3d                	cmp    al,0x3d
    129f:	0f 84 41 53 00 00    	je     1459 <__cxa_finalize@plt+0x3e9>
    12a5:	e8 b6 fd ff ff       	call   1060 <__ctype_b_loc@plt>
    12aa:	48 8b 10             	mov    rdx,QWORD PTR [rax]
    12ad:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    12b0:	48 63 c8             	movsxd rcx,eax
    12b3:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
    12b7:	48 01 6d             	add    rax,rcx
    12ba:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    12bd:	48 0f be c0          	movsx  rax,al
    12c1:	48 01 30             	add    rax,rax
    12c4:	48 01 d0             	add    rax,rdx
    12c7:	0f b7 00             	movzx  eax,WORD PTR [rax]
    12ca:	0f b7 6b             	movzx  eax,ax
    12cd:	83 e0 08             	and    eax,0x8
    12d0:	85 c0                	test   eax,eax
    12d2:	75 2c                	jne    1300 <__cxa_finalize@plt+0x290>
    12d4:	8b 45 65             	mov    eax,DWORD PTR [rbp-0x8]
    12d7:	48 63 d0             	movsxd rdx,eax
    12da:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
    12de:	48 01 d0             	add    rax,rdx
    12e1:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    12e4:	3c 2b                	cmp    al,0x2b
    12e6:	74 18                	je     1300 <__cxa_finalize@plt+0x290>
    12e8:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    12eb:	48 63 d0             	movsxd rdx,eax
    12ee:	48 8b 64 43          	mov    rax,QWORD PTR [rbp-0x38]
    12f2:	48 01 d0             	add    rax,rdx
    12f5:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    12f8:	3c 2f                	cmp    al,0x2f
    12fa:	0f 85 68 33 00 00    	jne    145c <__cxa_finalize@plt+0x3ec>
    1300:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    1303:	8d 50 01             	lea    edx,[rax+0x1]
    1306:	89 55 f8             	mov    DWORD PTR [rbp-0x8],edx
    1309:	48 63 d0             	movsxd rdx,eax
    130c:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
    1310:	48 01 d0             	add    rax,rdx
    1313:	0f b6 08             	movzx  ecx,BYTE PTR [rax]
    1316:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    1319:	8d 50 01             	lea    edx,[rax+0x1]
    131c:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
    131f:	89 ca                	mov    edx,ecx
    1321:	48 98                	cdqe   
    1323:	88 54 33 73          	mov    BYTE PTR [rbp+rax*1-0x27],dl
    1327:	83 7d fc 04          	cmp    DWORD PTR [rbp-0x4],0x4
    132b:	0f 85 11 01 00 00    	jne    1442 <__cxa_finalize@plt+0x3d2>
    1331:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
    1338:	eb 65                	jmp    1385 <__cxa_finalize@plt+0x315>
    133a:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
    1341:	eb 7d                	jmp    137b <__cxa_finalize@plt+0x30b>
    1343:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    1346:	48 98                	cdqe   
    1348:	0f b6 44 05 d9       	movzx  eax,BYTE PTR [rbp+rax*1-0x27]
    134d:	0f b6 d0             	movzx  edx,al
    1350:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
    1353:	48 98                	cdqe   
    1355:	48 8d 0d c4 0c 00 00 	lea    rcx,[rip+0xcc4]        # 2020 <__cxa_finalize@plt+0xfb0>
    135c:	0f b6 04 08          	movzx  eax,BYTE PTR [rax+rcx*1]
    1360:	0f be c0             	movsx  eax,al
    1363:	39 c2                	cmp    edx,eax
    1365:	75 10                	jne    1377 <__cxa_finalize@plt+0x307>
    1367:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
    136a:	89 c2                	mov    edx,eax
    136c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    136f:	48 98                	cdqe   
    1371:	88 54 05 d9          	mov    BYTE PTR [rbp+rax*1-0x27],dl
    1375:	eb 0a                	jmp    1381 <__cxa_finalize@plt+0x311>
    1377:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
    137b:	83 7d f4 3f          	cmp    DWORD PTR [rbp-0xc],0x3f
    137f:	7e c2                	jle    1343 <__cxa_finalize@plt+0x2d3>
    1381:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
    1385:	83 7d fc 03          	cmp    DWORD PTR [rbp-0x4],0x3
    1389:	7e af                	jle    133a <__cxa_finalize@plt+0x2ca>
    138b:	0f b6 45 d9          	movzx  eax,BYTE PTR [rbp-0x27]
    138f:	8d 14 85 00 00 00 00 	lea    edx,[rax*4+0x0]
    1396:	0f b6 45 da          	movzx  eax,BYTE PTR [rbp-0x26]
    139a:	0f b6 c0             	movzx  eax,al
    139d:	c1 f8 04             	sar    eax,0x4
    13a0:	83 e0 03             	and    eax,0x3
    13a3:	01 d0                	add    eax,edx
    13a5:	88 45 dd             	mov    BYTE PTR [rbp-0x23],al
    13a8:	0f b6 45 da          	movzx  eax,BYTE PTR [rbp-0x26]
    13ac:	0f b6 c0             	movzx  eax,al
    13af:	c1 e0 04             	shl    eax,0x4
    13b2:	89 c2                	mov    edx,eax
    13b4:	0f b6 45 db          	movzx  eax,BYTE PTR [rbp-0x25]
    13b8:	0f b6 c0             	movzx  eax,al
    13bb:	c1 f8 02             	sar    eax,0x2
    13be:	83 e0 0f             	and    eax,0xf
    13c1:	01 d0                	add    eax,edx
    13c3:	88 45 de             	mov    BYTE PTR [rbp-0x22],al
    13c6:	0f b6 45 db          	movzx  eax,BYTE PTR [rbp-0x25]
    13ca:	0f b6 c0             	movzx  eax,al
    13cd:	c1 e0 06             	shl    eax,0x6
    13d0:	89 c2                	mov    edx,eax
    13d2:	0f b6 45 dc          	movzx  eax,BYTE PTR [rbp-0x24]
    13d6:	01 d0                	add    eax,edx
    13d8:	88 45 df             	mov    BYTE PTR [rbp-0x21],al
    13db:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    13df:	48 8d 50 03          	lea    rdx,[rax+0x3]
    13e3:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
    13e7:	48 89 d6             	mov    rsi,rdx
    13ea:	48 89 c7             	mov    rdi,rax
    13ed:	e8 c3 fd ff ff       	call   11b5 <__cxa_finalize@plt+0x145>
    13f2:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
    13f6:	48 83 7d e0 00       	cmp    QWORD PTR [rbp-0x20],0x0
    13fb:	74 34                	je     1431 <__cxa_finalize@plt+0x3c1>
    13fd:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
    1404:	eb 23                	jmp    1429 <__cxa_finalize@plt+0x3b9>
    1406:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    140a:	48 8d 50 01          	lea    rdx,[rax+0x1]
    140e:	48 89 55 e8          	mov    QWORD PTR [rbp-0x18],rdx
    1412:	48 8b 55 e0          	mov    rdx,QWORD PTR [rbp-0x20]
    1416:	48 01 c2             	add    rdx,rax
    1419:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    141c:	48 98                	cdqe   
    141e:	0f b6 44 05 dd       	movzx  eax,BYTE PTR [rbp+rax*1-0x23]
    1423:	88 02                	mov    BYTE PTR [rdx],al
    1425:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
    1429:	83 7d fc 02          	cmp    DWORD PTR [rbp-0x4],0x2
    142d:	7e d7                	jle    1406 <__cxa_finalize@plt+0x396>
    142f:	eb 0a                	jmp    143b <__cxa_finalize@plt+0x3cb>
    1431:	b8 00 00 00 00       	mov    eax,0x0
    1436:	e9 ab 01 00 00       	jmp    15e6 <__cxa_finalize@plt+0x576>
    143b:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
    1442:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
    1446:	48 8d 50 ff          	lea    rdx,[rax-0x1]
    144a:	48 89 55 c0          	mov    QWORD PTR [rbp-0x40],rdx
    144e:	48 85 c0             	test   rax,rax
    1451:	0f 85 36 fe ff ff    	jne    128d <__cxa_finalize@plt+0x21d>
    1457:	eb 04                	jmp    145d <__cxa_finalize@plt+0x3ed>
    1459:	90                   	nop
    145a:	eb 01                	jmp    145d <__cxa_finalize@plt+0x3ed>
    145c:	90                   	nop
    145d:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
    1461:	0f 8e 30 01 00 00    	jle    1597 <__cxa_finalize@plt+0x527>
    1467:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    146a:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
    146d:	eb 0e                	jmp    147d <__cxa_finalize@plt+0x40d>
    146f:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    1472:	48 98                	cdqe   
    1474:	c6 44 05 d9 00       	mov    BYTE PTR [rbp+rax*1-0x27],0x0
    1479:	83 45 f8 01          	add    DWORD PTR [rbp-0x8],0x1
    147d:	83 7d f8 03          	cmp    DWORD PTR [rbp-0x8],0x3
    1481:	7e ec                	jle    146f <__cxa_finalize@plt+0x3ff>
    1483:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
    148a:	eb 4b                	jmp    14d7 <__cxa_finalize@plt+0x467>
    148c:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
    1493:	eb 38                	jmp    14cd <__cxa_finalize@plt+0x45d>
    1495:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    1498:	48 98                	cdqe   
    149a:	0f b6 44 05 d9       	movzx  eax,BYTE PTR [rbp+rax*1-0x27]
    149f:	0f b6 d0             	movzx  edx,al
    14a2:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
    14a5:	48 98                	cdqe   
    14a7:	48 8d 0d 72 0b 00 00 	lea    rcx,[rip+0xb72]        # 2020 <__cxa_finalize@plt+0xfb0>
    14ae:	0f b6 04 08          	movzx  eax,BYTE PTR [rax+rcx*1]
    14b2:	0f be c0             	movsx  eax,al
    14b5:	39 c2                	cmp    edx,eax
    14b7:	75 10                	jne    14c9 <__cxa_finalize@plt+0x459>
    14b9:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
    14bc:	89 c2                	mov    edx,eax
    14be:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    14c1:	48 98                	cdqe   
    14c3:	88 54 05 d9          	mov    BYTE PTR [rbp+rax*1-0x27],dl
    14c7:	eb 0a                	jmp    14d3 <__cxa_finalize@plt+0x463>
    14c9:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
    14cd:	83 7d f4 3f          	cmp    DWORD PTR [rbp-0xc],0x3f
    14d1:	7e c2                	jle    1495 <__cxa_finalize@plt+0x425>
    14d3:	83 45 f8 01          	add    DWORD PTR [rbp-0x8],0x1
    14d7:	83 7d f8 03          	cmp    DWORD PTR [rbp-0x8],0x3
    14db:	7e af                	jle    148c <__cxa_finalize@plt+0x41c>
    14dd:	0f b6 45 d9          	movzx  eax,BYTE PTR [rbp-0x27]
    14e1:	8d 14 85 00 00 00 00 	lea    edx,[rax*4+0x0]
    14e8:	0f b6 45 da          	movzx  eax,BYTE PTR [rbp-0x26]
    14ec:	0f b6 c0             	movzx  eax,al
    14ef:	c1 f8 04             	sar    eax,0x4
    14f2:	83 e0 03             	and    eax,0x3
    14f5:	01 d0                	add    eax,edx
    14f7:	88 45 dd             	mov    BYTE PTR [rbp-0x23],al
    14fa:	0f b6 45 da          	movzx  eax,BYTE PTR [rbp-0x26]
    14fe:	0f b6 c0             	movzx  eax,al
    1501:	c1 e0 04             	shl    eax,0x4
    1504:	89 c2                	mov    edx,eax
    1506:	0f b6 45 db          	movzx  eax,BYTE PTR [rbp-0x25]
    150a:	0f b6 c0             	movzx  eax,al
    150d:	c1 f8 02             	sar    eax,0x2
    1510:	83 e0 0f             	and    eax,0xf
    1513:	01 d0                	add    eax,edx
    1515:	88 45 de             	mov    BYTE PTR [rbp-0x22],al
    1518:	0f b6 45 db          	movzx  eax,BYTE PTR [rbp-0x25]
    151c:	0f b6 c0             	movzx  eax,al
    151f:	c1 e0 06             	shl    eax,0x6
    1522:	89 c2                	mov    edx,eax
    1524:	0f b6 45 dc          	movzx  eax,BYTE PTR [rbp-0x24]
    1528:	01 d0                	add    eax,edx
    152a:	88 45 df             	mov    BYTE PTR [rbp-0x21],al
    152d:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    1530:	83 e8 01             	sub    eax,0x1
    1533:	48 63 d0             	movsxd rdx,eax
    1536:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    153a:	48 01 c2             	add    rdx,rax
    153d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
    1541:	48 89 d6             	mov    rsi,rdx
    1544:	48 89 c7             	mov    rdi,rax
    1547:	e8 69 fc ff ff       	call   11b5 <__cxa_finalize@plt+0x145>
    154c:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
    1550:	48 83 7d e0 00       	cmp    QWORD PTR [rbp-0x20],0x0
    1555:	74 39                	je     1590 <__cxa_finalize@plt+0x520>
    1557:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
    155e:	eb 23                	jmp    1583 <__cxa_finalize@plt+0x513>
    1560:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    1564:	48 8d 50 01          	lea    rdx,[rax+0x1]
    1568:	48 89 55 e8          	mov    QWORD PTR [rbp-0x18],rdx
    156c:	48 8b 55 e0          	mov    rdx,QWORD PTR [rbp-0x20]
    1570:	48 01 c2             	add    rdx,rax
    1573:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    1576:	48 98                	cdqe   
    1578:	0f b6 44 05 dd       	movzx  eax,BYTE PTR [rbp+rax*1-0x23]
    157d:	88 02                	mov    BYTE PTR [rdx],al
    157f:	83 45 f8 01          	add    DWORD PTR [rbp-0x8],0x1
    1583:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    1586:	83 e8 01             	sub    eax,0x1
    1589:	39 45 f8             	cmp    DWORD PTR [rbp-0x8],eax
    158c:	7c d2                	jl     1560 <__cxa_finalize@plt+0x4f0>
    158e:	eb 07                	jmp    1597 <__cxa_finalize@plt+0x527>
    1590:	b8 00 00 00 00       	mov    eax,0x0
    1595:	eb 4f                	jmp    15e6 <__cxa_finalize@plt+0x576>
    1597:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    159b:	48 8d 50 01          	lea    rdx,[rax+0x1]
    159f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
    15a3:	48 89 d6             	mov    rsi,rdx
    15a6:	48 89 c7             	mov    rdi,rax
    15a9:	e8 07 fc ff ff       	call   11b5 <__cxa_finalize@plt+0x145>
    15ae:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
    15b2:	48 83 7d e0 00       	cmp    QWORD PTR [rbp-0x20],0x0
    15b7:	74 17                	je     15d0 <__cxa_finalize@plt+0x560>
    15b9:	48 8b 55 e0          	mov    rdx,QWORD PTR [rbp-0x20]
    15bd:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    15c1:	48 01 d0             	add    rax,rdx
    15c4:	c6 00 00             	mov    BYTE PTR [rax],0x0
    15c7:	48 83 7d b8 00       	cmp    QWORD PTR [rbp-0x48],0x0
    15cc:	74 14                	je     15e2 <__cxa_finalize@plt+0x572>
    15ce:	eb 07                	jmp    15d7 <__cxa_finalize@plt+0x567>
    15d0:	b8 00 00 00 00       	mov    eax,0x0
    15d5:	eb 0f                	jmp    15e6 <__cxa_finalize@plt+0x576>
    15d7:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
    15db:	48 8b 55 e8          	mov    rdx,QWORD PTR [rbp-0x18]
    15df:	48 89 10             	mov    QWORD PTR [rax],rdx
    15e2:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
    15e6:	c9                   	leave  
    15e7:	c3                   	ret    
