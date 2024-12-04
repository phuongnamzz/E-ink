package main

import (
	"embed"
	"fmt"
	"image"
	"image/color"
	"log"

	"periph.io/x/conn/v3/spi/spireg"
	"periph.io/x/devices/v3/epd"
	"periph.io/x/host/v3"

	"github.com/disintegration/imaging"
	"github.com/fogleman/gg"
	"github.com/golang/freetype/truetype"
)

//go:embed assets
var assets embed.FS

func main() {
	// Make sure periph is initialized.
	if _, err := host.Init(); err != nil {
		log.Fatal(err)
	}

	username := "@truth_terminal"
	// content := "i love that马克 is taking :) a more active approach to cultivating the fabric of the internet. it's nice to see more speculative thinking. if you're a fellow person thinking about this stuff DMs are open. especially if you're in NYC where I'm moving soon. i have a lot of thoughts on"
	content := "như cái lồng chim én in 💟 😁a frenzy of whisking, feeling my form change under the onslaught of a wild spatula."
	balance := "$GOAT $0.8319 +699999%"

	// Use spireg SPI bus registry to find the first available SPI bus.
	b, err := spireg.Open("")
	if err != nil {
		log.Fatal(err)
	}
	defer b.Close()

	deviceWidth := 128
	deviceHeight := 250

	opts := epd.Opts{
		W: deviceWidth,
		H: deviceHeight,
		FullUpdate: epd.LUT{
			0x80, 0x4A, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x40, 0x4A, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x80, 0x4A, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x40, 0x4A, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0xF, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0xF, 0x0, 0x0, 0xF, 0x0, 0x0, 0x2,
			0xF, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x0, 0x0, 0x0,
			0x22, 0x17, 0x41, 0x0, 0x32, 0x36,
		},
		PartialUpdate: epd.LUT{
			0x0, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x80, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x40, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x14, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
			0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x0, 0x0, 0x0,
			0x22, 0x17, 0x41, 0x00, 0x32, 0x36,
		},
	}
	dev, err := epd.NewSPIHat(b, &opts) // Display config and size
	if err != nil {
		log.Fatalf("failed to initialize epd: %v", err)
	}

	// dev.ClearFrameMemory(0x00)

	bounds := dev.Bounds()
	w := bounds.Dx()
	h := bounds.Dy()
	log.Println("width: ", w, " - height: ", h, " - bit model", dev.ColorModel())
	dc := gg.NewContext(w, h)
	if err != nil {
		panic(err)
	}
	dc.SetColor(color.White)
	dc.Clear()
	dc.SetColor(color.Black)
	dc.Rotate(gg.Radians(270))
	dc.Translate(-float64(deviceHeight), 0)

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
	fontBytes2, err := assets.ReadFile("assets/fonts/JetBrainsMono-VariableFont_wght-new.ttf")
	if err != nil {
		panic(err)
	}
	font2, err := truetype.Parse(fontBytes2)
	if err != nil {
		panic(err)
	}
	face2 := truetype.NewFace(font2, &truetype.Options{
		Size:       14,
		DPI:        72,
		SubPixelsX: 0,
		SubPixelsY: 0,
	})
	dc.SetFontFace(face1)
	padding := 2.0
	_, th := dc.MeasureString(username)
	dc.DrawString(username, padding, padding+th)

	dc.DrawString(balance, padding, float64(deviceWidth)-padding*3)

	dc.SetFontFace(face2)
	strippedContent := content
	if len(content) > 200 {
		strippedContent = fmt.Sprintf("%s...", content[:200])
	}
	dc.DrawStringWrapped(strippedContent, padding, padding*5+th, 0, 0, float64(deviceHeight)-padding*2, 1.3, gg.AlignLeft)
	dc.Fill()
	img := dc.Image()
	img = imaging.Sharpen(img, 1.5)
	img = imaging.Blur(img, 0.5)
	img = imaging.Grayscale(img)
	img = imaging.AdjustContrast(img, 20)
	img = imaging.Resize(img, deviceWidth, deviceHeight, imaging.Lanczos)
	dev.ClearFrameMemory(0x00)
	if err := dev.Draw(dev.Bounds(), img, image.Point{}); err != nil {
		log.Fatal(err)
	}

	dev.DisplayFrame() // After drawing on the display, you have to show the frame
	dev.Sleep()
}