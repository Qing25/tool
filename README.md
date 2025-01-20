

将 KQA Pro 的 KoPL 转为 工具调用



KoPL: https://github.com/THU-KEG/KoPL

执行例子
```python
engine.FilterStr(engine.FilterConcept(engine.FindAll(), "region of France"), "SIREN number","200053403")
(['Q18677875'], [{'key': 'SIREN number', 'value': <kopl.util.ValueClass object at 0x700ea7638b30>, 'qualifiers': {}}])

```