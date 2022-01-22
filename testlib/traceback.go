package testlib

import (
	"sort"
)

type elem struct {
	_type bool
	time  int64
	index int
}

func Trace(in *bufferW, out *bufferW) (string, error) {
	var elems []elem
	for i := range in.monotime {
		elems = append(elems, elem{
			_type: true,
			time:  in.monotime[i],
			index: i,
		})
	}
	for j := range out.monotime {
		elems = append(elems, elem{
			_type: false,
			time:  out.monotime[j],
			index: j,
		})
	}

	if len(elems) == 0 {
		return "", nil
	}

	sort.SliceStable(elems, func(i, j int) bool {
		return elems[i].time < elems[j].time
	})

	var trace []byte
	//var t = !elems[0]._type
	for k := range elems {
		//if elems[k]._type && !t {
		//	trace = append(trace, []byte("> ")...)
		//}
		//t = elems[k]._type

		if elems[k]._type {
			var b, err = in.ReadByte()
			if err != nil {
				return string(trace), err
			}
			trace = append(trace, b)
		} else {
			var b, err = out.ReadByte()
			if err != nil {
				return string(trace), err
			}
			trace = append(trace, b)
		}
	}

	return string(trace), nil
}
