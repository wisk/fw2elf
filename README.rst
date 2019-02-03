Firmware to ELF
===============


Introduction
------------

This python script allows to convert a raw firmware image to an ELF file.
The ELF file could also contain more information, like: interrupts vector, IO registers, etc.

.. image:: https://github.com/wisk/fw2elf/raw/master/iv.png

.. image:: https://github.com/wisk/fw2elf/raw/master/vtor.png


Supported features
------------------

+-----------+------------------+------------------+----------------------+
| Name      | Auto map address | Auto entry point | Structures           |
+===========+==================+==================+======================+
| Cortex-M3 | Yes              | Yes              | Interrupts vector    |
|           |                  |                  | System control space |
+-----------+------------------+------------------+----------------------+