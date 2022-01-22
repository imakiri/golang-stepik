package testlib

import (
	"bytes"
	"github.com/golang-collections/go-datastructures/bitarray"
)

func Traceback(buf *bytes.Buffer, ba bitarray.BitArray, index uint64) (string, error) {
	if index == 0 {
		return "", nil
	}

	//fmt.Println(index, buf.Len())

	var traceback []byte
	var output, err = ba.GetBit(0)
	if err != nil {
		return "", err
	}

	if !output {
		traceback = append(traceback, []byte("> ")...)
	}

	var b byte
	if b, err = buf.ReadByte(); err != nil {
		return string(traceback), nil
	}
	traceback = append(traceback, b)
	var previous = output

	for i := uint64(1); i < index; i++ {
		if output, err = ba.GetBit(i); err != nil {
			return "", err
		}

		if !output && (output != previous) {
			traceback = append(traceback, []byte("> ")...)
		}

		if b, err = buf.ReadByte(); err != nil {
			return string(traceback), nil
		}

		traceback = append(traceback, b)
		previous = output
	}

	return string(traceback), nil
}
