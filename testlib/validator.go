package testlib

type validator struct{}

func (v *validator) Validate(code string) error {
	return nil
}

func NewValidator() (*validator, error) {
	var v = new(validator)
	return v, nil
}
