# BaseAny

BaseAny的基本逻辑是，在用户给定任意一个长度的字符串后，仅用这些字符串来构建一套编码体系。

根据信息熵，如果用户给定了64个可打印字符，那么根据编码理论，我们就可以使用这64个字符表示一个6个比特的信息。

Base64就是这样的一种编码体系，它使用了64个可打印字符来表示6个比特的信息。

对于BaseAny而言，工作流程与Base64类似，给定一个任意长度的字符集，计算他的信息熵，然后将原信息拆分表示，最后填充。

## BaseAny的工作流程

### 获取字符集Mapping List
Mapping List 是一个由待映射字符组成的列表，需要满足以下条件：

1. 有序
2. 无重复
3. 长度合适
4. 可打印

MappingList能表示的信息熵为：`log2(len(MappingList))` 既可用位数available digits是信息熵向下取整的结果。

### LengthConstrain

对于MappingList而言，要想正确表示信息，需要对长度做出限制。

而具体的限制方式是和对齐的方式有关的。

在Base64中，在比特序列不是3的倍数时，需要填充0，这种填充0称之为对齐填充。algin padding。因为在Base64中，使用64个可表示字符来表示6个比特的信息，所以在对齐填充时，需要4个或者2个比特的0。

但在用户给定的任意MappingList中，可能存在不是2的倍数的情况，尤其是如果available digits与8的最小公约数为1时，就需要缺几个0补几个0。

在这种情况下，随着available digits的增大，需要补充的0的个数也会增大，这样就会导致编码效率的降低。

为了解决过多的补充0的问题，因此提出了一个新的填充方案，即CountPadding。

在CountPadding中，我们保留一系列可打印字符表示我们补充的0的个数。

例如在available digits为3时，我们可能需要补充1个或者2个0，那么我们就可以使用两个可打印字符来表示这两种情况。

这就需要补充0的预留字符是available digits数-1。

### CountPadding

CountPadding的工作流程如下：

1. 获取MappingList的长度
2. 计算MappingList的信息熵，并向下取整获得avaiable digits，既[`log2(len(MappingList))`] (AD)
3. 计算CountPadding的预留字符数，既`available digits - 1` (Count Padding Number CPN)
4. 计算MappingList是否有足够多的字符来表示预留字符数，既 2^AD + CPN = Minumum Length (ML) <= len(MappingList)

### AlignPadding

AlignPadding的工作流程如下：
1. 获取MappingList的长度
2. 计算MappingList的信息熵，并向下取整获得avaiable digits，既[`log2(len(MappingList))`] (AD)
3. 计算CountPadding的预留字符数，在AlignPadding中，(Align Padding Number APN) = 1
4. 计算是否有至少一个字符来表示预留字符数，既 2^AD + CPN = Minumum Length (ML) <= len(MappingList)

### BaseAny的编码流程

1. 获取MappingList的基本信息，包括Available Digits, *PN(CPN or APN), Minumum Length(ML)
2. 构建MappingList的编码表(mapping index->char)和反向查询表(reverse_mapping char->index)
3. 获取MappingList的对齐方式，既CountPadding or AlignPadding
4. 根据对齐方式获取填充逻辑所需要的字符，如果是CP，那就是一系列字符，如果是AP，那就是一个字符
5. 拆解原数据，将Bytes拆解成Bits序列，并填充0

