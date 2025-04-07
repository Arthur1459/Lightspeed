make-app:
	$(MAKE) download-requirements
	pyinstaller -F --noconsole -i="./rsc/misc/icon.png" --name "Lightspeed"\
				--add-data "rsc/*.*:rsc/" \
				\
				--add-data "rsc/maps/*.pkl:rsc/maps/" \
				--add-data "rsc/maps/world_1/*.pkl:rsc/maps/world_1/" \
				--add-data "rsc/maps/world_2/*.pkl:rsc/maps/world_2/" \
				--add-data "rsc/maps/world_3/*.pkl:rsc/maps/world_3/" \
				--add-data "rsc/maps/world_4/*.pkl:rsc/maps/world_4/" \
				\
			  	--add-data "rsc/visuals/*.*:rsc/visuals/" \
			  	--add-data "rsc/visuals/player/stand/*.png:rsc/visuals/player/stand/" \
			  	--add-data "rsc/visuals/player/run/*.png:rsc/visuals/player/run/" \
			  	--add-data "rsc/visuals/player/jumpside/*.png:rsc/visuals/player/jumpside/" \
			  	--add-data "rsc/visuals/player/fall/*.png:rsc/visuals/player/fall/" \
			  	--add-data "rsc/visuals/player/slide/*.png:rsc/visuals/player/slide/" \
			  	--add-data "rsc/visuals/player/grapple/*.png:rsc/visuals/player/grapple/" \
			  	--add-data "rsc/visuals/blocks/blocks/*.png:rsc/visuals/blocks/blocks/" \
			  	--add-data "rsc/visuals/blocks/blocks_top/*.png:rsc/visuals/blocks/blocks_top/" \
			  	--add-data "rsc/visuals/blocks/fire_blocks/*.png:rsc/visuals/blocks/fire_blocks/" \
			  	--add-data "rsc/visuals/blocks/fire_blocks/*.png:rsc/visuals/blocks/fire_blocks/" \
			  	--add-data "rsc/visuals/particles/default/*.png:rsc/visuals/particles/default/" \
			  	--add-data "rsc/visuals/particles/fire/*.png:rsc/visuals/particles/fire/" \
			  	--add-data "rsc/visuals/particles/star/*.png:rsc/visuals/particles/star/" \
			  	--add-data "rsc/visuals/particles/void/*.png:rsc/visuals/particles/void/" \
			  	--add-data "rsc/visuals/creatures/bat/*.png:rsc/visuals/creatures/bat/" \
			  	--add-data "rsc/visuals/misc/start/*.png:rsc/visuals/misc/start/" \
			  	--add-data "rsc/visuals/misc/end/*.png:rsc/visuals/misc/end/" \
			  	--add-data "rsc/visuals/misc/*.png:rsc/visuals/misc/" \
			  	--add-data "rsc/visuals/gui/*.png:rsc/visuals/gui/" \
			  	--add-data "rsc/visuals/gui/PressButton/*.png:rsc/visuals/gui/PressButton/" \
			  	--add-data "rsc/visuals/gui/PressButton/frame/*.png:rsc/visuals/gui/PressButton/frame/" \
			  	--add-data "rsc/visuals/gui/SwitchButton/*.png:rsc/visuals/gui/SwitchButton/" \
			  	\
			  	--add-data "rsc/sounds/musics/ingame/*.mp3:rsc/sounds/musics/ingame/" \
			  	--add-data "rsc/sounds/musics/menu/*.mp3:rsc/sounds/musics/menu/" \
			  	--add-data "rsc/sounds/sfx/*.mp3:rsc/sounds/sfx/" \
			  	\
			  	--add-data "rsc/videos/*.mp4:rsc/videos/" \
			  	\
			  	--add-data "rsc/misc/*.*:rsc/misc/" \
			  	\
			  	main.py
	$(MAKE) tag-executable

download-requirements:
	pip3 install pyinstaller
	pip3 install glob2
	pip3 install opencv-python
	pip3 install pygame

tag-executable:
	chmod +x "./dist/Lightspeed"
	chmod +x "./dist/Lightspeed.app"
