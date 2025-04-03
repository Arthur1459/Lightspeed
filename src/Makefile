make-app: download-requirements
	pyinstaller -F --noconsole -i="./rsc/misc/icon.png" --name "Lightspeed"\
				--add-data "rsc/*.*:rsc/" \
				\
				--add-data "rsc/maps/*.pkl:rsc/maps/" \
				\
			  	--add-data "rsc/visuals/*.*:rsc/visuals/" \
			  	--add-data "rsc/visuals/player/stand/*.png:rsc/visuals/player/stand/" \
			  	--add-data "rsc/visuals/player/run/*.png:rsc/visuals/player/run/" \
			  	--add-data "rsc/visuals/player/jumpside/*.png:rsc/visuals/player/jumpside/" \
			  	--add-data "rsc/visuals/player/fall/*.png:rsc/visuals/player/fall/" \
			  	--add-data "rsc/visuals/player/slide/*.png:rsc/visuals/player/slide/" \
			  	--add-data "rsc/visuals/player/dead/*.png:rsc/visuals/player/dead/" \
			  	--add-data "rsc/visuals/player/grapple/*.png:rsc/visuals/player/grapple/" \
			  	--add-data "rsc/visuals/blocks/metal_blocks/*.png:rsc/visuals/blocks/metal_blocks/" \
			  	--add-data "rsc/visuals/blocks/fire_blocks/*.png:rsc/visuals/blocks/fire_blocks/" \
			  	--add-data "rsc/visuals/blocks/fire_blocks/*.png:rsc/visuals/blocks/fire_blocks/" \
			  	--add-data "rsc/visuals/particles/default/*.png:rsc/visuals/particles/default/" \
			  	--add-data "rsc/visuals/particles/fire/*.png:rsc/visuals/particles/fire/" \
			  	--add-data "rsc/visuals/particles/star/*.png:rsc/visuals/particles/star/" \
			  	--add-data "rsc/visuals/particles/void/*.png:rsc/visuals/particles/void/" \
			  	--add-data "rsc/visuals/creatures/bat/*.png:rsc/visuals/creatures/bat/" \
			  	\
			  	--add-data "rsc/sounds/musics/ingame/*.mp3:rsc/sounds/musics/ingame/" \
			  	\
			  	--add-data "rsc/videos/*.mp4:rsc/videos/" \
			  	\
			  	--add-data "rsc/misc/*.*:rsc/misc/" \
			  	main.py

download-requirements:
	pip3 install pyinstaller
	pip3 install glob2
	pip3 install opencv-python
	pip3 install pygame
