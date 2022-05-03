package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestAssert(t *testing.T) {
	hoge := "nil"
	assert.NotNil(t, hoge)
}
