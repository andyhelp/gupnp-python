all: 	test1.c
	gcc -I/usr/local/include/gupnp-1.0 -I/usr/local/include/gssdp-1.0 -I/usr/include/libxml2 -I/usr/include/libsoup-2.4 -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include -I/usr/include/gtk-2.0 -I/usr/lib/gtk-2.0/include -I/usr/include/atk-1.0 -I/usr/include/cairo -I/usr/include/pango-1.0 -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include -I/usr/include/pixman-1 -I/usr/include/freetype2 -I/usr/include/libpng12 -pthread -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include -I../.. -DDATA_DIR=\"/usr/local/share/gupnp-tools\" -g -O2 -Wall -o gupnp_test -pthread -Wl,--export-dynamic  -L/usr/local/lib /usr/local/lib/libgupnp-1.0.so -L/usr/lib -luuid /usr/local/lib/libgssdp-1.0.so /usr/lib/libsoup-2.4.so /usr/lib/libxml2.so /usr/lib/libgnutls.so /usr/lib/libtasn1.so /usr/lib/libgcrypt.so /usr/lib/libgpg-error.so /usr/lib/libgtk-x11-2.0.so /usr/lib/libgdk-x11-2.0.so /usr/lib/libatk-1.0.so /usr/lib/libgdk_pixbuf-2.0.so /usr/lib/libgio-2.0.so /usr/lib/libpangocairo-1.0.so /usr/lib/libpangoft2-1.0.so /usr/lib/libcairo.so /usr/lib/libpixman-1.so /usr/lib/libglitz-glx.so /usr/lib/libGL.so /usr/lib/libXext.so /usr/lib/libglitz.so /usr/lib/libpng12.so /usr/lib/libXrender.so /usr/lib/libX11.so /usr/lib/libXau.so /usr/lib/libXdmcp.so /usr/lib/libpango-1.0.so -lm /usr/lib/libfontconfig.so /usr/lib/libfreetype.so -lz /usr/lib/libexpat.so /usr/lib/libgobject-2.0.so /usr/lib/libgmodule-2.0.so -ldl /usr/lib/libgthread-2.0.so -lpthread -lrt /usr/lib/libglib-2.0.so  -pthread test1.c

segv: 	segv.c
	gcc -I/usr/local/include/gupnp-1.0 -I/usr/local/include/gssdp-1.0 -I/usr/include/libxml2 -I/usr/include/libsoup-2.4 -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include -I/usr/include/gtk-2.0  \
	-I/usr/lib/gtk-2.0/include -I/usr/include/atk-1.0 -I/usr/include/cairo -I/usr/include/pango-1.0 -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include -I/usr/include/pixman-1 -I/usr/include/freetype2 \
	-I/usr/include/libpng12 -pthread -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include -I../.. -DDATA_DIR=\"/usr/local/share/gupnp-tools\" -g -O2 -Wall -o segv_test -pthread -Wl,--export-dynamic  \
	-L/usr/local/lib /usr/local/lib/libgupnp-1.0.so -L/usr/lib -luuid /usr/local/lib/libgssdp-1.0.so /usr/lib/libsoup-2.4.so /usr/lib/libxml2.so /usr/lib/libgnutls.so /usr/lib/libtasn1.so \
	/usr/lib/libgcrypt.so /usr/lib/libgpg-error.so /usr/lib/libgtk-x11-2.0.so /usr/lib/libgdk-x11-2.0.so /usr/lib/libatk-1.0.so /usr/lib/libgdk_pixbuf-2.0.so /usr/lib/libgio-2.0.so \
	/usr/lib/libpangocairo-1.0.so /usr/lib/libpangoft2-1.0.so /usr/lib/libcairo.so /usr/lib/libpixman-1.so /usr/lib/libglitz-glx.so /usr/lib/libGL.so /usr/lib/libXext.so /usr/lib/libglitz.so \
	/usr/lib/libpng12.so /usr/lib/libXrender.so /usr/lib/libX11.so /usr/lib/libXau.so /usr/lib/libXdmcp.so /usr/lib/libpango-1.0.so -lm /usr/lib/libfontconfig.so /usr/lib/libfreetype.so -lz \
	/usr/lib/libexpat.so /usr/lib/libgobject-2.0.so /usr/lib/libgmodule-2.0.so -ldl /usr/lib/libgthread-2.0.so -lpthread -lrt /usr/lib/libglib-2.0.so  -pthread segv.c 

segv-1.0.gir:
	g-ir-scanner -v --add-include-path=. \
	--noclosure \
        --output $@ \
	--namespace segv \
 	--library=gupnp-1.0 \
        --nsversion=1.0 \
	segv.h segv.c

segv-1.0.typelib: segv-1.0.gir
	g-ir-compiler --includedir=. -o $@ segv-1.0.gir
