Module(
    body=[
        Import(
            names=[
                alias(name='os')]),
        If(
            test=UnaryOp(
                op=Not(),
                operand=Call(
                    func=Attribute(
                        value=Attribute(
                            value=Name(id='os', ctx=Load()),
                            attr='path',
                            ctx=Load()),
                        attr='exists',
                        ctx=Load()),
                    args=[
                        Constant(value='license.txt')],
                    keywords=[])),
            body=[
                Expr(
                    value=Call(
                        func=Attribute(
                            value=Name(id='sys', ctx=Load()),
                            attr='exit',
                            ctx=Load()),
                        args=[
                            Constant(value='File does not exist.')],
                        keywords=[]))],
            orelse=[]),
        With(
            items=[
                withitem(
                    context_expr=Call(
                        func=Name(id='open', ctx=Load()),
                        args=[
                            Constant(value='license.txt')],
                        keywords=[]),
                    optional_vars=Name(id='f', ctx=Store()))],
            body=[
                Assign(
                    targets=[
                        Name(id='key', ctx=Store())],
                    value=Call(
                        func=Attribute(
                            value=Name(id='f', ctx=Load()),
                            attr='read',
                            ctx=Load()),
                        args=[],
                        keywords=[]))]),
        If(
            test=UnaryOp(
                op=Not(),
                operand=Compare(
                    left=Call(
                        func=Name(id='len', ctx=Load()),
                        args=[
                            Name(id='key', ctx=Load())],
                        keywords=[]),
                    ops=[
                        Eq()],
                    comparators=[
                        Constant(value=64)])),
            body=[
                Raise(
                    exc=Call(
                        func=Name(id='Exception', ctx=Load()),
                        args=[
                            Constant(value='Wrong key')],
                        keywords=[]))],
            orelse=[]),
        Assign(
            targets=[
                Name(id='key1', ctx=Store())],
            value=Subscript(
                value=Name(id='key', ctx=Load()),
                slice=Slice(
                    upper=Constant(value=16)),
                ctx=Load())),
        Assign(
            targets=[
                Name(id='key2', ctx=Store())],
            value=Subscript(
                value=Name(id='key', ctx=Load()),
                slice=Slice(
                    lower=Constant(value=16),
                    upper=Constant(value=32)),
                ctx=Load())),
        Assign(
            targets=[
                Name(id='key3', ctx=Store())],
            value=Subscript(
                value=Name(id='key', ctx=Load()),
                slice=Slice(
                    lower=Constant(value=32),
                    upper=Constant(value=48)),
                ctx=Load())),
        Assign(
            targets=[
                Name(id='key4', ctx=Store())],
            value=Subscript(
                value=Name(id='key', ctx=Load()),
                slice=Slice(
                    lower=Constant(value=48),
                    upper=Constant(value=64)),
                ctx=Load())),
        ClassDef(
            name='KeyChkr',
            bases=[],
            keywords=[],
            body=[
                FunctionDef(
                    name='__init__',
                    args=arguments(
                        posonlyargs=[],
                        args=[
                            arg(arg='self'),
                            arg(arg='k')],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[]),
                    body=[
                        Assign(
                            targets=[
                                Attribute(
                                    value=Name(id='self', ctx=Load()),
                                    attr='k',
                                    ctx=Store())],
                            value=Name(id='k', ctx=Load()))],
                    decorator_list=[]),
                FunctionDef(
                    name='check',
                    args=arguments(
                        posonlyargs=[],
                        args=[
                            arg(arg='self')],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[]),
                    body=[
                        Assign(
                            targets=[
                                Name(id='k', ctx=Store())],
                            value=Call(
                                func=Attribute(
                                    value=Call(
                                        func=Attribute(
                                            value=Attribute(
                                                value=Name(id='self', ctx=Load()),
                                                attr='k',
                                                ctx=Load()),
                                            attr='upper',
                                            ctx=Load()),
                                        args=[],
                                        keywords=[]),
                                    attr='lower',
                                    ctx=Load()),
                                args=[],
                                keywords=[])),
                        If(
                            test=Compare(
                                left=Name(id='k', ctx=Load()),
                                ops=[
                                    Eq()],
                                comparators=[
                                    Constant(value='you_solved_it!!}')]),
                            body=[
                                Return(
                                    value=Constant(value=True))],
                            orelse=[
                                Return(
                                    value=Constant(value=False))])],
                    decorator_list=[])],
            decorator_list=[]),
        Assign(
            targets=[
                Name(id='ok', ctx=Store())],
            value=Constant(value=False)),
        If(
            test=Compare(
                left=Subscript(
                    value=Name(id='key', ctx=Load()),
                    slice=Constant(value=0),
                    ctx=Load()),
                ops=[
                    Eq()],
                comparators=[
                    Constant(value='E')]),
            body=[
                If(
                    test=Compare(
                        left=Subscript(
                            value=Name(id='key', ctx=Load()),
                            slice=Constant(value=1),
                            ctx=Load()),
                        ops=[
                            Eq()],
                        comparators=[
                            Constant(value='N')]),
                    body=[
                        If(
                            test=Compare(
                                left=Subscript(
                                    value=Name(id='key', ctx=Load()),
                                    slice=Constant(value=2),
                                    ctx=Load()),
                                ops=[
                                    Eq()],
                                comparators=[
                                    Constant(value='O')]),
                            body=[
                                If(
                                    test=Compare(
                                        left=Subscript(
                                            value=Name(id='key', ctx=Load()),
                                            slice=Constant(value=3),
                                            ctx=Load()),
                                        ops=[
                                            Eq()],
                                        comparators=[
                                            Constant(value='{')]),
                                    body=[
                                        If(
                                            test=Compare(
                                                left=Subscript(
                                                    value=Name(id='key', ctx=Load()),
                                                    slice=Constant(value=4),
                                                    ctx=Load()),
                                                ops=[
                                                    Eq()],
                                                comparators=[
                                                    Constant(value='L')]),
                                            body=[
                                                If(
                                                    test=Compare(
                                                        left=Subscript(
                                                            value=Name(id='key', ctx=Load()),
                                                            slice=Constant(value=5),
                                                            ctx=Load()),
                                                        ops=[
                                                            Eq()],
                                                        comparators=[
                                                            Constant(value='1')]),
                                                    body=[
                                                        If(
                                                            test=Compare(
                                                                left=Subscript(
                                                                    value=Name(id='key', ctx=Load()),
                                                                    slice=Constant(value=6),
                                                                    ctx=Load()),
                                                                ops=[
                                                                    Eq()],
                                                                comparators=[
                                                                    Constant(value='3')]),
                                                            body=[
                                                                If(
                                                                    test=Compare(
                                                                        left=Subscript(
                                                                            value=Name(id='key', ctx=Load()),
                                                                            slice=Constant(value=7),
                                                                            ctx=Load()),
                                                                        ops=[
                                                                            Eq()],
                                                                        comparators=[
                                                                            Constant(value='3')]),
                                                                    body=[
                                                                        If(
                                                                            test=Compare(
                                                                                left=Subscript(
                                                                                    value=Name(id='key', ctx=Load()),
                                                                                    slice=Constant(value=8),
                                                                                    ctx=Load()),
                                                                                ops=[
                                                                                    Eq()],
                                                                                comparators=[
                                                                                    Constant(value='3')]),
                                                                            body=[
                                                                                If(
                                                                                    test=Compare(
                                                                                        left=Subscript(
                                                                                            value=Name(id='key', ctx=Load()),
                                                                                            slice=Constant(value=9),
                                                                                            ctx=Load()),
                                                                                        ops=[
                                                                                            Eq()],
                                                                                        comparators=[
                                                                                            Constant(value='3')]),
                                                                                    body=[
                                                                                        If(
                                                                                            test=Compare(
                                                                                                left=Subscript(
                                                                                                    value=Name(id='key', ctx=Load()),
                                                                                                    slice=Constant(value=10),
                                                                                                    ctx=Load()),
                                                                                                ops=[
                                                                                                    Eq()],
                                                                                                comparators=[
                                                                                                    Constant(value='3')]),
                                                                                            body=[
                                                                                                If(
                                                                                                    test=Compare(
                                                                                                        left=Subscript(
                                                                                                            value=Name(id='key', ctx=Load()),
                                                                                                            slice=Constant(value=11),
                                                                                                            ctx=Load()),
                                                                                                        ops=[
                                                                                                            Eq()],
                                                                                                        comparators=[
                                                                                                            Constant(value='3')]),
                                                                                                    body=[
                                                                                                        If(
                                                                                                            test=Compare(
                                                                                                                left=Subscript(
                                                                                                                    value=Name(id='key', ctx=Load()),
                                                                                                                    slice=Constant(value=12),
                                                                                                                    ctx=Load()),
                                                                                                                ops=[
                                                                                                                    Eq()],
                                                                                                                comparators=[
                                                                                                                    Constant(value='3')]),
                                                                                                            body=[
                                                                                                                If(
                                                                                                                    test=Compare(
                                                                                                                        left=Subscript(
                                                                                                                            value=Name(id='key', ctx=Load()),
                                                                                                                            slice=Constant(value=13),
                                                                                                                            ctx=Load()),
                                                                                                                        ops=[
                                                                                                                            Eq()],
                                                                                                                        comparators=[
                                                                                                                            Constant(value='3')]),
                                                                                                                    body=[
                                                                                                                        If(
                                                                                                                            test=Compare(
                                                                                                                                left=Subscript(
                                                                                                                                    value=Name(id='key', ctx=Load()),
                                                                                                                                    slice=Constant(value=14),
                                                                                                                                    ctx=Load()),
                                                                                                                                ops=[
                                                                                                                                    Eq()],
                                                                                                                                comparators=[
                                                                                                                                    Constant(value='3')]),
                                                                                                                            body=[
                                                                                                                                If(
                                                                                                                                    test=Compare(
                                                                                                                                        left=Subscript(
                                                                                                                                            value=Name(id='key', ctx=Load()),
                                                                                                                                            slice=Constant(value=15),
                                                                                                                                            ctx=Load()),
                                                                                                                                        ops=[
                                                                                                                                            Eq()],
                                                                                                                                        comparators=[
                                                                                                                                            Constant(value='3')]),
                                                                                                                                    body=[
                                                                                                                                        Assign(
                                                                                                                                            targets=[
                                                                                                                                                Name(id='ok', ctx=Store())],
                                                                                                                                            value=Constant(value=True))],
                                                                                                                                    orelse=[
                                                                                                                                        Assign(
                                                                                                                                            targets=[
                                                                                                                                                Name(id='ok', ctx=Store())],
                                                                                                                                            value=Constant(value=False))])],
                                                                                                                            orelse=[
                                                                                                                                Assign(
                                                                                                                                    targets=[
                                                                                                                                        Name(id='ok', ctx=Store())],
                                                                                                                                    value=Constant(value=False))])],
                                                                                                                    orelse=[
                                                                                                                        Assign(
                                                                                                                            targets=[
                                                                                                                                Name(id='ok', ctx=Store())],
                                                                                                                            value=Constant(value=False))])],
                                                                                                            orelse=[
                                                                                                                Assign(
                                                                                                                    targets=[
                                                                                                                        Name(id='ok', ctx=Store())],
                                                                                                                    value=Constant(value=False))])],
                                                                                                    orelse=[
                                                                                                        Assign(
                                                                                                            targets=[
                                                                                                                Name(id='ok', ctx=Store())],
                                                                                                            value=Constant(value=False))])],
                                                                                            orelse=[
                                                                                                Assign(
                                                                                                    targets=[
                                                                                                        Name(id='ok', ctx=Store())],
                                                                                                    value=Constant(value=False))])],
                                                                                    orelse=[
                                                                                        Assign(
                                                                                            targets=[
                                                                                                Name(id='ok', ctx=Store())],
                                                                                            value=Constant(value=False))])],
                                                                            orelse=[
                                                                                Assign(
                                                                                    targets=[
                                                                                        Name(id='ok', ctx=Store())],
                                                                                    value=Constant(value=False))])],
                                                                    orelse=[
                                                                        Assign(
                                                                            targets=[
                                                                                Name(id='ok', ctx=Store())],
                                                                            value=Constant(value=False))])],
                                                            orelse=[
                                                                Assign(
                                                                    targets=[
                                                                        Name(id='ok', ctx=Store())],
                                                                    value=Constant(value=False))])],
                                                    orelse=[
                                                        Assign(
                                                            targets=[
                                                                Name(id='ok', ctx=Store())],
                                                            value=Constant(value=False))])],
                                            orelse=[
                                                Assign(
                                                    targets=[
                                                        Name(id='ok', ctx=Store())],
                                                    value=Constant(value=False))])],
                                    orelse=[
                                        Assign(
                                            targets=[
                                                Name(id='ok', ctx=Store())],
                                            value=Constant(value=False))])],
                            orelse=[
                                Assign(
                                    targets=[
                                        Name(id='ok', ctx=Store())],
                                    value=Constant(value=False))])],
                    orelse=[
                        Assign(
                            targets=[
                                Name(id='ok', ctx=Store())],
                            value=Constant(value=False))])],
            orelse=[
                Assign(
                    targets=[
                        Name(id='ok', ctx=Store())],
                    value=Constant(value=False))]),
        Assign(
            targets=[
                Name(id='vals', ctx=Store())],
            value=List(
                elts=[
                    Constant(value=36),
                    Constant(value=76),
                    Constant(value=96),
                    Constant(value=102),
                    Constant(value=99),
                    Constant(value=118),
                    Constant(value=97),
                    Constant(value=76),
                    Constant(value=119),
                    Constant(value=102),
                    Constant(value=99),
                    Constant(value=118),
                    Constant(value=97),
                    Constant(value=76),
                    Constant(value=124),
                    Constant(value=120)],
                ctx=Load())),
        For(
            target=Tuple(
                elts=[
                    Name(id='i', ctx=Store()),
                    Name(id='k', ctx=Store())],
                ctx=Store()),
            iter=Call(
                func=Name(id='enumerate', ctx=Load()),
                args=[
                    Name(id='key2', ctx=Load())],
                keywords=[]),
            body=[
                Assign(
                    targets=[
                        Name(id='v', ctx=Store())],
                    value=BinOp(
                        left=Call(
                            func=Name(id='ord', ctx=Load()),
                            args=[
                                Subscript(
                                    value=Name(id='key2', ctx=Load()),
                                    slice=Name(id='i', ctx=Load()),
                                    ctx=Load())],
                            keywords=[]),
                        op=BitXor(),
                        right=Constant(value=19))),
                If(
                    test=Compare(
                        left=Name(id='v', ctx=Load()),
                        ops=[
                            NotEq()],
                        comparators=[
                            Subscript(
                                value=Name(id='vals', ctx=Load()),
                                slice=Name(id='i', ctx=Load()),
                                ctx=Load())]),
                    body=[
                        Assign(
                            targets=[
                                Name(id='ok', ctx=Store())],
                            value=Constant(value=False))],
                    orelse=[])],
            orelse=[]),
        FunctionDef(
            name='check_key',
            args=arguments(
                posonlyargs=[],
                args=[
                    arg(arg='k')],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]),
            body=[
                If(
                    test=Compare(
                        left=Subscript(
                            value=Name(id='k', ctx=Load()),
                            slice=Slice(
                                step=UnaryOp(
                                    op=USub(),
                                    operand=Constant(value=1))),
                            ctx=Load()),
                        ops=[
                            NotEq()],
                        comparators=[
                            Constant(value='_!ftcnocllunlol_')]),
                    body=[
                        Return(
                            value=Constant(value=False))],
                    orelse=[]),
                Return(
                    value=Constant(value=True))],
            decorator_list=[]),
        If(
            test=UnaryOp(
                op=Not(),
                operand=Call(
                    func=Name(id='check_key', ctx=Load()),
                    args=[
                        Name(id='key3', ctx=Load())],
                    keywords=[])),
            body=[
                Assign(
                    targets=[
                        Name(id='ok', ctx=Store())],
                    value=Constant(value=False))],
            orelse=[]),
        Assign(
            targets=[
                Name(id='chk', ctx=Store())],
            value=Call(
                func=Name(id='KeyChkr', ctx=Load()),
                args=[
                    Name(id='key4', ctx=Load())],
                keywords=[])),
        Assign(
            targets=[
                Name(id='ok', ctx=Store())],
            value=Call(
                func=Attribute(
                    value=Name(id='chk', ctx=Load()),
                    attr='check',
                    ctx=Load()),
                args=[],
                keywords=[])),
        If(
            test=Name(id='ok', ctx=Load()),
            body=[
                Expr(
                    value=Call(
                        func=Name(id='print', ctx=Load()),
                        args=[
                            Constant(value='Correct license!')],
                        keywords=[]))],
            orelse=[
                Expr(
                    value=Call(
                        func=Name(id='print', ctx=Load()),
                        args=[
                            Constant(value='Nope')],
                        keywords=[]))])],
    type_ignores=[])