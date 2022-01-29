package working

import (
	"io"
	"time"
)

type Validator interface {
	Validate(code string) error
}

type Tester interface {
	Test(handler io.ReadWriter) bool
}

type Handler interface {
	io.ReadWriteCloser
}

type Test interface {
	Args() []string
	Timeout() time.Duration
	Delay() time.Duration
	Feedback() string
	Error() error
	Validator
	Tester
}
