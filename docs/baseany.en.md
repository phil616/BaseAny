
# BaseAny

more for docs/baseany.md

The basic logic of BaseAny is that after the user gives a string of any length, only these strings are used to build an encoding system.

According to information entropy, if the user gives 64 printable characters, then according to coding theory, we can use these 64 characters to represent a 6-bit information.

Base64 is such an encoding system, which uses 64 printable characters to represent 6 bits of information.

For BaseAny, the workflow is similar to Base64. Given a character set of any length, calculate its information entropy, then split the original information to represent it, and finally fill it.

## BaseAny’s workflow

### Get character set Mapping List
Mapping List is a list of characters to be mapped, which needs to meet the following conditions:

1. orderly
2. No duplication
3. Suitable length
4. Printable

The information entropy that MappingList can represent is: `log2(len(MappingList))`. Available digits are the result of rounding down the information entropy.

### LengthConstrain

For MappingList, in order to correctly represent information, the length needs to be limited.

The specific restriction method is related to the alignment method.

In Base64, when the bit sequence is not a multiple of 3, it needs to be padded with 0s. This padding of 0s is called alignment padding. Algin padding. Because in Base64, 64 representable characters are used to represent 6 bits of information, 4 or 2 bits of 0 are required when aligning padding.

However, in any MappingList given by the user, there may be cases that are not multiples of 2. Especially if the least common divisor of available digits and 8 is 1, several missing 0s need to be filled in.

In this case, as the available digits increase, the number of 0s that need to be supplemented will also increase, which will lead to a reduction in coding efficiency.

In order to solve the problem of too many supplementary 0s, a new padding scheme is proposed, namely CountPadding.

In CountPadding, we reserve a series of printable characters to represent the number of 0s we add.

For example, when available digits is 3, we may need to add 1 or 2 0s, then we can use two printable characters to represent these two situations.

This requires adding 0. The reserved characters are available digits -1.

### CountPadding

The workflow of CountPadding is as follows:

1. Get the length of MappingList
2. Calculate the information entropy of MappingList and round down to obtain available digits, which is [`log2(len(MappingList))`] (AD)
3. Calculate the number of reserved characters for CountPadding, that is, `available digits - 1` (Count Padding Number CPN)
4. Calculate whether MappingList has enough characters to represent the number of reserved characters, that is, 2^AD + CPN = Minumum Length (ML) <= len(MappingList)

### AlignPadding

The workflow of AlignPadding is as follows:
1. Get the length of MappingList
2. Calculate the information entropy of MappingList and round down to obtain available digits, which is [`log2(len(MappingList))`] (AD)
3. Calculate the number of reserved characters for CountPadding. In AlignPadding, (Align Padding Number APN) = 1
4. Calculate whether there is at least one character to represent the number of reserved characters, that is, 2^AD + CPN = Minumum Length (ML) <= len(MappingList)

### BaseAny coding process

1. Get the basic information of MappingList, including Available Digits, *PN(CPN or APN), Minimum Length(ML)
2. Construct the coding table (mapping index->char) and reverse query table (reverse_mapping char->index) of MappingList
3. Get the alignment of MappingList, either CountPadding or AlignPadding
4. Obtain the characters required for the filling logic according to the alignment. If it is CP, it is a series of characters. If it is AP, it is one character.
5. Disassemble the original data, disassemble Bytes into Bits sequence, and fill it with 0