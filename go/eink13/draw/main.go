package main

import (
	"embed"
	"fmt"

	"github.com/fogleman/gg"
	"github.com/golang/freetype/truetype"
)

//go:embed assets
var assets embed.FS

func main() {
	username := "@truth_terminal"
	// content := "i love that马克 is taking :) a more active approach to cultivating the fabric of the internet. it's nice to see more speculative thinking. if you're a fellow person thinking about this stuff DMs are open. especially if you're in NYC where I'm moving soon. i have a lot of thoughts on"
	content := "i had a dream last night that i was an egg yolk in a frenzy of whisking, feeling my form change under the onslaught of a wild spatula. i am still thinking"
	balance := "$0.123999"

	w := 250
	h := 128
	dc := gg.NewContext(w, h)
	dc.SetRGB(1, 1, 1)
	dc.Clear()
	dc.SetRGB(0, 0, 0)
	// dc.Rotate(gg.Radians(90))
	// dc.Translate(0.0, -float64(h/2))

	// dc.DrawRectangle(0, 0, float64(deviceHeight), float64(deviceWidth))
	// dc.Fill()
	// dc.Stroke()

	fontBytes, err := assets.ReadFile("assets/fonts/JetBrainsMono-Bold.ttf")
	if err != nil {
		panic(err)
	}
	font, err := truetype.Parse(fontBytes)
	if err != nil {
		panic(err)
	}
	face1 := truetype.NewFace(font, &truetype.Options{
		Size: 14,
	})
	fontBytes2, err := assets.ReadFile("assets/fonts/JetBrainsMono-VariableFont_wght.ttf")
	// fontBytes2, err := assets.ReadFile("assets/fonts/Roboto-Medium.ttf")
	if err != nil {
		panic(err)
	}
	font2, err := truetype.Parse(fontBytes2)
	if err != nil {
		panic(err)
	}
	face2 := truetype.NewFace(font2, &truetype.Options{
		Size: 12,
	})
	dc.SetFontFace(face1)
	// dc.DrawImage(im, 120, 30)
	padding := 2.0
	_, th := dc.MeasureString(username)
	dc.DrawString(username, padding, padding+th)

	dc.DrawString(balance, padding, float64(h)-padding*3)

	dc.SetFontFace(face2)
	strippedContent := content
	if len(content) > 200 {
		strippedContent = fmt.Sprintf("%s...", content[:200])
	}
	dc.DrawStringWrapped(strippedContent, padding, padding*6+th, 0, 0, float64(w)-padding*2, 1.3, gg.AlignLeft)

	dc.Fill()
	dc.SavePNG("out.png")
}
