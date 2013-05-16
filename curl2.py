import pycurl, StringIO, random, time
# Function que realiza las conexiones curl
def curl(args):
	# Variables
	dev_null = StringIO.StringIO()


	crCurl      = pycurl.Curl();
	sUrl        = args.get( 'url', None );
	sPostField  = args.get( 'post', None );
	ckCookie    = args.get( 'cookie', None );
	nHeader     = args.get( 'header', 0 );
	fcWrite     = args.get( 'write', dev_null.write );
	nTimeOut    = args.get( 'time_out', 30 );
	sAgent      = args.get( 'agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8' );
	sReferer    = args.get( 'referer', '-' );
	aReferer    = args.get( 'aReferer', None );
	aProxys     = args.get( 'proxy', None );
	nProxyTunel = args.get( 'proxy_tunel', 1 );
	aHeader     = args.get( 'http_header', [ 'Accept: image/gif, image/x-bitmap, image/jpeg, image/pjpeg', 'Connection: Keep-Alive', 'Content-type: application/x-www-form-urlencoded;charset=UTF-8' ] );
	nFollow     = args.get( 'follow_location', 1 );
	sUserPasswd = args.get( 'user_passwd', None );

	if sUrl is None:
		return false;

    # Comprobamos si nos han pasado un array con referers para modificar el referer
	if aReferer is not None:
		# Referer aleatorio
		nRandomRf = random.randint( 0, len( aReferer ) - 1 );
		sReferer = aReferer[nRandomRf].replace( '[curl_text]', sReferer );

	# Opciones
	crCurl.setopt( crCurl.URL, sUrl );
	crCurl.setopt( crCurl.HEADER, nHeader );
	crCurl.setopt( crCurl.WRITEFUNCTION, fcWrite );
	crCurl.setopt( crCurl.HTTPHEADER, aHeader );
	crCurl.setopt( crCurl.CONNECTTIMEOUT, nTimeOut );
	crCurl.setopt( crCurl.REFERER, sReferer );
	crCurl.setopt( crCurl.USERAGENT, sAgent );
	crCurl.setopt( crCurl.FOLLOWLOCATION, nFollow );
	crCurl.setopt( crCurl.VERBOSE, 1 );
	if sUserPasswd is not None:
		crCurl.setopt( crCurl.USERPWD, sUserPasswd );

	if aProxys is not None:
		# Usamos random para ir cambiando entre los diferentes proxys, asi no realizamos las peticiones siempre con el mismo proxy
		nRandom = random.randint( 0, len( aProxys ) - 1 );
		crCurl.setopt( crCurl.HTTPPROXYTUNNEL, nProxyTunel );
		crCurl.setopt( crCurl.PROXY, aProxys[nRandom] );

	if sPostField is not None:
		crCurl.setopt( crCurl.POST, 1 );
		crCurl.setopt( crCurl.POSTFIELDS, sPostField );

	if ckCookie is not None:
		crCurl.setopt( crCurl.COOKIEJAR, ckCookie );
		crCurl.setopt( crCurl.COOKIEFILE, ckCookie );

	crCurl.perform()

	# Comprobamos que la peticion es correcta, de no ser esperamos 10 segundos y volvemos a realizarla
	if crCurl.getinfo( crCurl.HTTP_CODE ) != 200:
		time.sleep(10);
		curl(args);

