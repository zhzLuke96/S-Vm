# lambda

# f.x.x
欧耶，完事~

就是这么简单，要学会一眼看到底，你才抓得住lambda的真谛

# f.x.f(x)
替换！绑定的不换！

遗留问题：自由变量并不能判断，这个暂时忽略

# f.x.f(f(x))
函数，调用就是替换！

遗留问题：由于function被设置为`不可规约`的，在function中的call将不会被`简化`，这也是由于我们省略了`自由变量`产生

# f.x.f(f(f(x)))
interpreter:

    这么简单的东西就不用库了
    （其实就是懒得,用`库`的话会有很多很多好处，非常麻烦的`智能检查`和`语法提示`，要手写的话，还是有点不爽不爽）
    其实对象行为都定义好了，`解释器`就是一个翻译流程变成代码的过程

    我这里的解释器（建立AST树）基本分作三块：`拍散`（tokenize），`层次化`（parse_token），`标记为对象`（sign）

    流水线看上去是这样的=>
    eval_lamb := __TOKEN__ |> tokenize |> parse_token |> sign

    INPUT : (x.(y.(x y)))
    => ['(', 'x', '.', '(', 'y', '.', '(', 'x', 'y', ')', ')', ')']
    => ['x', '.', ['y', '.', ['x', 'y']]]
    => <object> (<object>.toString() => (x.(y.(x y))))

# f.x.f(f(f(f(x))))
变量搞毛线？

解决遗留问题

    function的规约，我们`直接开启`试试看会如何
    => ((x.(p.(x.(p ((x p) x))))) (p.(x.(p x))))
    这条之前为化解的句子(p.(x.(p (((p.(x.(p x))) p) x))))
    被错误的化解成了 (p.(x.(p ((x p) x))))

    太长了我们简单点看问题所在
    (((p.(x.(p x))) p) x) => ((x p) x)
    (((p.(x.(p x))) p) x) => (p x)
    什么鬼啊！多出来了还行

    好吧其实不是这里的问题，我们看整个过程，
    ((x.((n.(p.(x.(p ((n p) x))))) x)) (p.(x.(p x))))
    这句里有两个x.也就是`两个lambda`绑定了变量`x`，但是其实，其中有一点`局部变量`的意思，即应该是这样
    ((x.((n.(p.(x1.(p ((n p) x1))))) x)) (p1.(x2.(p1 x2))))

    翻译成过程就是，function中每个重名的绑定变量都重命名新名字
    耶，撒花~（这是个`取巧`的做法，变相解决同名问题）
    等等！
    (x.y) m这里面的m咋办？没在function里面的？对啊！
    f((x.x(f x))) x => x.(x(x x))明显是错误的，也要改名！

    走你，自由变量改为f，绑定变量改为b，加上计数器

> tips:值得注意的，这里我给var对象增加了isfree属性，并默认为true，整个解析流程均用不到，只有最后规约的时候会用，本来可以在规约时标注，但是自由绑定毕竟是本身的值，加在里面很优雅嘛

# f.x.f(f(f(f(f(x)))))
最基本的推导工作至少要能给程序命名吧...好，我们试试看

    a = 1;b = a + 1;
    b中的a算啥？对，引用，最简单的替换就行（当然有别的弄法）

    哇，难道要改interpreter？nono，lambda引用就放倒env中就完事了，每次解析式子之前，看有没有有的话替换那个位置

    tips：我们在这里要限定每个引用名不得为一个小写字母，也就是默认一个小写字母的调用通常作为变量使用而不是引用

    该怎么定义呢？a=b这样显然一点也不像函数式，我们就如下表示定义一个在全局环境中的引用，并且不会解析和规约
    (define zero (f.(x.(x))))

    tips: 引用？看上去很简单，但是，总是会出错？？明明已经做得完美的替换局部变量名为什么还会重复？原来，引用时如果只是浅拷贝的话自然会改变的很莫名其妙，深拷贝怎么搞啊，又得遍历一遍ast？
    噗...这样就完事了！
```python
    LCObjCpy = lambda LCobj : eval_lamb(str(LCobj))
```
cool!

# f.x.f(f(f(f(f((f(x))))))
标题也许你懂，但是我自己都乱不清了，怎么输出成数字？怎么对接LC function和python函数呢？这里我们就试试解决这个问题
