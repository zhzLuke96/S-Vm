<h1 align="center">纸上得来终觉浅,欲知此事要躬行</h1>

<h5 align="center"><small>Powered by: Game Scripting Mastery (USA)Alex.Varanese </small></h5>

# README
面向高级语言的软`虚拟机`，准备用JS和PY都搞搞看

基本上交叉了计科所有内容，大目标的话是实现在这个虚拟机上运行的`lisp方言解释器`


# 试水
```javascript
var REG = {AX:0,BX:0,CX:0,IP:0,IR:true} // IR:isRuning
var code = "" // some code
var STACK = [] // just STACK.pop or push , not set SP option in REG

ver fetch = ()=>code[REG.IP]
var _eval = function(_inst_){
    switch(_inst_){
        // PSH,POP,ADD,SUB,SET,HTL,JMP
    }
}
var run = function(){
    while(REG.IR){
        _eval(fetch());
        REG.IP+=1;
    }
}
```
结构非常简单，甚至寄存器直接操作的是动态数据，但是结果是很让人兴奋的：
```javascript
var code = `SET AX 1
SET BX 1
SET CX 10
ADD AX BX
DIS AX
ADD BX AX
DIS BX
SUB CX 1
JMP 3
HTL`.split("\n")
```
（果然汇编不是人写的，那么简单的功能编成这么粗糙的汇编仍然难以看懂）
<br>CX用来控制循环条件，这个程序将求解斐波那契数第3-13个，并打印出来

# 
