<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gmi="http://www.isotc211.org/2005/gmi"  xmlns:srv="http://www.isotc211.org/2005/srv" xmlns:gmx="http://www.isotc211.org/2005/gmx" xmlns:gsr="http://www.isotc211.org/2005/gsr" xmlns:gss="http://www.isotc211.org/2005/gss" xmlns:gts="http://www.isotc211.org/2005/gts" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:date="http://exslt.org/dates-and-times" xmlns:str="http://exslt.org/strings" exclude-result-prefixes='date'>
	<!-- Updated stylesheet for OneStop project according to OneStop guidelines, removed unused variables, etc.; thomas.jaensch@noaa.gov spring 2016 -->
	<!--Original stylesheet was from ncISO software http://www.ngdc.noaa.gov/eds/tds/; the xslt was modified by NCEI-MD to work directly with netCDF data; yuanjie.li@noaa.gov 3/1/2013-->
	<xsl:output method="xml" encoding="UTF-8" indent="yes"/>
	<xsl:variable name="stylesheetVersion" select="'2.21'"/>
	<xsl:strip-space elements="*"/>
	<xsl:variable name="smallcase" select="'abcdefghijklmnopqrstuvwxyz'"/>
	<xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"/>
	<xsl:variable name="physicalMeasurementCnt" select="count(netcdf/variable[not(contains((translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')),'_qc'))])"/>
	<xsl:variable name="qualityInformationCnt" select="count(netcdf/variable[contains((translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')),'_qc')])"/>
	<xsl:variable name="standardNameCnt" select="count(netcdf/variable/attribute[@name='standard_name'])"/>
	
<!-- Identifier Fields: 4 possible -->
	<!--NCEI-MD modified to Pathfinder data-->
	<xsl:variable name="id" select="netcdf/attribute[@name='title']/@value"/>
	<xsl:variable name="title" select="netcdf/attribute[@name='title']/@value"/>
	<xsl:variable name="datasetname" select="'NDBC-CMANWx'"/>	
	<xsl:variable name="filesize" select="netcdf/filesize"/>
	<xsl:variable name="fileidentifier" select="netcdf/title"/>
	<xsl:variable name="englishtitle" select="netcdf/englishtitle"/>
	<xsl:variable name="browsegraphic" select="translate(normalize-space(concat('http://maps.googleapis.com/maps/api/staticmap?center=', netcdf/attribute[@name='geospatial_lat_min']/@value,',',netcdf/attribute[@name='geospatial_lon_min']/@value, '&amp;zoom=10&amp;scale=false&amp;size=600x600&amp;maptype=satellite&amp;format=png&amp;visual_refresh=true&amp;markers=color:red%7C', netcdf/attribute[@name='geospatial_lat_min']/@value,',',netcdf/attribute[@name='geospatial_lon_min']/@value, '&amp;stream=true&amp;stream_ID=plot_image')),' ','')"/>

	<!-- Service Fields: 4 possible -->
	<!--Need to edit based on the Pathfinder data-->
	<xsl:variable name="thredds_netcdfsubsetCnt" select="count(netcdf/group[@name='Dataservicelinks']/group[@name='services']/attribute[@name='nccs_service'])"/>
	
<!--NCEI-MD added for extra service links -->
	<xsl:variable name="Pathfinderthredds" select="normalize-space(concat('http://data.nodc.noaa.gov/thredds/catalog/', netcdf/path, 'catalog.html?dataset=',netcdf/path,netcdf/title,'.nc'))"/>
	<xsl:variable name="Pathfinderhttp" select="normalize-space(concat('http://data.nodc.noaa.gov/', netcdf/path,netcdf/title,'.nc'))"/>
	<xsl:variable name="Pathfinderopendap" select="normalize-space(concat('http://data.nodc.noaa.gov/thredds/dodsC/', netcdf/path,netcdf/title,'.nc.html'))"/>
	<xsl:variable name="Pathfinderftp" select="normalize-space(concat('ftp://ftp.nodc.noaa.gov/pub/data.nodc/',netcdf/path,netcdf/title,'.nc'))"/>
	
	<!--Added for Cloud pilot project-->
	<xsl:variable name="serviceMax">7</xsl:variable>

	<!-- Text Search Fields: 7 possible -->
	<!--Need to check with Pathfinder data-->
	<xsl:variable name="summary" select="netcdf/attribute[@name='summary']/@value"/>
	<xsl:variable name="keywords" select="netcdf/attribute[@name='keywords']/@value"/>
	<xsl:variable name="keywordsVocabulary" select="netcdf/attribute[@name='keywords_vocabulary']/@value"/>
	<xsl:variable name="stdNameVocabulary" select="netcdf/attribute[@name='standard_name_vocabulary']/@value"/>
	<xsl:variable name="comment" select="netcdf/attribute[@name='comment']/@value"/>
	<xsl:variable name="history" select="netcdf/attribute[@name='history']/@value"/>
	
<!-- Extent Search Fields: 17 possible -->

	<xsl:variable name="geospatial_lat_min" select="netcdf/attribute[@name='geospatial_lat_min']/@value"/>
	<xsl:variable name="geospatial_lat_max" select="netcdf/attribute[@name='geospatial_lat_max']/@value"/>
	<xsl:variable name="geospatial_lon_min" select="netcdf/attribute[@name='geospatial_lon_min']/@value"/>
	<xsl:variable name="geospatial_lon_max" select="netcdf/attribute[@name='geospatial_lon_max']/@value"/>
	
	
	<xsl:variable name="timeStart" select="netcdf/attribute[@name='time_coverage_start']/@value"/>
	<xsl:variable name="timeEnd" select="netcdf/attribute[@name='time_coverage_end']/@value"/>
	<xsl:variable name="verticalMin" select="netcdf/group[@name='CFMetadata']/attribute[@name='geospatial_vertical_min']/@value"/>
	<xsl:variable name="verticalMax" select="netcdf/attribute[@name='geospatial_vertical_max']/@value"/>
	<xsl:variable name="geospatial_lat_units" select="//attribute[@name='geospatial_lat_units']/@value"/>
	<xsl:variable name="geospatial_lon_units" select="//attribute[@name='geospatial_lon_units']/@value"/>
	<xsl:variable name="temporalUnits" select="'1'"/>
	<xsl:variable name="verticalUnits" select="//attribute[@name='geospatial_vertical_units']/@value"/>
	<xsl:variable name="geospatial_lat_resolution" select="//attribute[@name='geospatial_lat_resolution']/@value"/>
	<xsl:variable name="geospatial_lon_resolution" select="//attribute[@name='geospatial_lon_resolution']/@value"/>
	<xsl:variable name="timeResolution" select="'1'"/>
	<xsl:variable name="timeDuration" select="'1'"/>
	<xsl:variable name="verticalResolution" select=" //attribute[@name='geospatial_vertical_resolution']/@value"/>
	<xsl:variable name="verticalPositive" select="netcdf/attribute[@name='geospatial_vertical_positive']/@value"/>
	<!-- dimension variables -->
	
<!--Need to check with Pathfinder-->
	<xsl:variable name="longitudeVariableName" select="netcdf/variable[@name='lon']/attribute[@name='standard_name']/@value"/>
	<xsl:variable name="latitudeVariableName" select="netcdf/variable[@name='lat']/attribute[@name='standard_name' ]/@value"/>
	<xsl:variable name="verticalVariableName" select="netcdf/variable/attribute[@name='positive' and (@value='up' or @value='down')]/@value"/>
	<xsl:variable name="timeVariableName" select="netcdf/variable/attribute[@name='standard_name' and (translate(@value,ABCDEFGHIJKLMNOPQRSTUVWXYZ,abcdefghijklmnopqrstuvwxyz))='time']/@value"/>

	<!--  Extent Totals -->
	<xsl:variable name="extentTotal" select=" count($timeStart) + count($timeEnd)"/>

	<!-- Responsible Party Fields: 14 possible -->
	<!--Need to update based on Pathfinder-->
	<xsl:variable name="creatorName" select="netcdf/attribute[@name='creator_name']/@value"/>
	<xsl:variable name="creatorURL" select="netcdf/attribute[@name='creator_url']/@value"/>
	<xsl:variable name="creatorEmail" select="netcdf/attribute[@name='creator_email']/@value"/>
	<xsl:variable name="creatorDate" select="netcdf/attribute[@name='date_created']/@value"/>
	<xsl:variable name="modifiedDate" select="netcdf/attribute[@name='date_modified']/@value"/>
	<xsl:variable name="issuedDate" select="netcdf/attribute[@name='date_issued']/@value"/>
	<!--updated by NCEI-MD, all the contact inforation for granule level data is using NCEI-MD's customer service info-->
	<xsl:variable name="institution" select="'US DOC; NOAA; National Centers for Environmental Information'"/>
	<xsl:variable name="project" select="netcdf/attribute[@name='project']/@value"/>
	<xsl:variable name="acknowledgment" select="netcdf/attribute[@name='acknowledgment']/@value"/>
	<xsl:variable name="dateCnt" select="count($creatorDate) + count($modifiedDate) + count($issuedDate)"/>
	<xsl:variable name="creatorTotal" select="'1'"/>

	   <!-- Data contributor  -->
	<xsl:variable name="contributorName"  select="netcdf/attribute[@name='contributor_name']/@value"/>
	<xsl:variable name="contributorRole"  select="netcdf/attribute[@name='contributor_role']/@value"/>
	<xsl:variable name="contributorTotal"  select="count($contributorName) + count($contributorRole)"/>

	<!-- Data publisher -->
	<xsl:variable name="publisherName"  select="'National Centers for Environmental Information (NCEI)'"/>
	<xsl:variable name="publisherURL"  select="'https://www.ncei.noaa.gov/'"/>
	<xsl:variable name="publisherEmail"  select="'NCEI.info@noaa.gov'"/>
	<xsl:variable name="publisherTotal"  select="'3'"/>

	<!-- Other Fields: 2 possible -->
	<xsl:variable name="cdmType" select="netcdf/attribute[@name='cdm_data_type']/@value"/>
	<xsl:variable name="license" select="netcdf/attribute[@name='license']/@value"/>

	<!--    Write ISO Metadata  -->

	<xsl:template match="/">
		<gmi:MI_Metadata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:srv="http://www.isotc211.org/2005/srv" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gsr="http://www.isotc211.org/2005/gsr" xmlns:gss="http://www.isotc211.org/2005/gss" xmlns:gts="http://www.isotc211.org/2005/gts" xmlns:gmi="http://www.isotc211.org/2005/gmi" xmlns:gmx="http://www.isotc211.org/2005/gmx" xsi:schemaLocation="http://www.isotc211.org/2005/gmi http://www.ngdc.noaa.gov/metadata/published/xsd/schema.xsd">
			<gmd:fileIdentifier>
				<xsl:call-template name="writeCharacterString">
					<xsl:with-param name="stringToWrite" select="concat($datasetname,'.',$fileidentifier)"/>
				</xsl:call-template>
			</gmd:fileIdentifier>
			<gmd:language>
				<gco:CharacterString>eng; USA</gco:CharacterString>
			</gmd:language>
			<gmd:characterSet>
				<gmd:MD_CharacterSetCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode" codeListValue="utf8">utf8</gmd:MD_CharacterSetCode>
			</gmd:characterSet>
			<gmd:parentIdentifier>
				<gmx:Anchor xlink:href="http://data.nodc.noaa.gov/cgi-bin/iso?id=gov.noaa.nodc:NDBC-CMANWx" xlink:actuate="onRequest" xlink:title="Collection ID">gov.noaa.nodc:NDBC-CMANWx</gmx:Anchor>
			</gmd:parentIdentifier>
			<gmd:hierarchyLevel>
				<gmd:MD_ScopeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ScopeCode" codeListValue="dataset">dataset</gmd:MD_ScopeCode>
			</gmd:hierarchyLevel>
			<gmd:hierarchyLevelName>
				<gco:CharacterString>Granule</gco:CharacterString>
			</gmd:hierarchyLevelName>
			<!-- metadata contact is creator -->
			<!-- <gmd:contact gco:nilReason="withheld"/> -->
			<gmd:contact>
				<gmd:CI_ResponsibleParty>
					<gmd:organisationName>
						<gco:CharacterString>
							DOC/NOAA/NESDIS/NCEI &gt; National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce
						</gco:CharacterString>
					</gmd:organisationName>
					<gmd:positionName>
						<gco:CharacterString>Data Officer</gco:CharacterString>
					</gmd:positionName>
					<gmd:contactInfo>
						<gmd:CI_Contact>
							<gmd:phone>
								<gmd:CI_Telephone>
									<gmd:voice>
										<gco:CharacterString>301-713-3277</gco:CharacterString>
									</gmd:voice>
									<gmd:facsimile>
										<gco:CharacterString>301-713-3300</gco:CharacterString>
									</gmd:facsimile>
								</gmd:CI_Telephone>
							</gmd:phone>
							<gmd:address>
								<gmd:CI_Address>
									<gmd:deliveryPoint>
										<gco:CharacterString>Federal Building 151 Patton Avenue</gco:CharacterString>
									</gmd:deliveryPoint>
									<gmd:city>
										<gco:CharacterString>Asheville</gco:CharacterString>
									</gmd:city>
									<gmd:administrativeArea>
										<gco:CharacterString>NC</gco:CharacterString>
									</gmd:administrativeArea>
									<gmd:postalCode>
										<gco:CharacterString>28801-5001</gco:CharacterString>
									</gmd:postalCode>
									<gmd:country>
										<gco:CharacterString>USA</gco:CharacterString>
									</gmd:country>
									<gmd:electronicMailAddress>
										<gco:CharacterString>NODC.DataOfficer@noaa.gov</gco:CharacterString>
									</gmd:electronicMailAddress>
								</gmd:CI_Address>
							</gmd:address>
							<gmd:onlineResource>
								<gmd:CI_OnlineResource>
									<gmd:linkage>
										<gmd:URL>https://www.ncei.noaa.gov/</gmd:URL>
									</gmd:linkage>
									<gmd:protocol>
										<gco:CharacterString>HTTP</gco:CharacterString>
									</gmd:protocol>
									<gmd:applicationProfile>
										<gco:CharacterString>Standard Internet browser</gco:CharacterString>
									</gmd:applicationProfile>
									<gmd:name>
										<gco:CharacterString>
											NOAA National Centers for Environmental Information website
										</gco:CharacterString>
									</gmd:name>
									<gmd:description>
										<gco:CharacterString>
											Main NCEI website providing links to access data and data services.
										</gco:CharacterString>
									</gmd:description>
									<gmd:function>
										<gmd:CI_OnLineFunctionCode codeList="http://www.ngdc.noaa.gov/metadata/published/xsd/schema/resources/Codelist/gmxCodelists.xml#CI_OnLineFunctionCode" codeListValue="information">information</gmd:CI_OnLineFunctionCode>
									</gmd:function>
								</gmd:CI_OnlineResource>
							</gmd:onlineResource>
						</gmd:CI_Contact>
					</gmd:contactInfo>
					<gmd:role>
						<gmd:CI_RoleCode codeList="http://www.ngdc.noaa.gov/metadata/published/xsd/schema/resources/Codelist/gmxCodelists.xml#CI_RoleCode" codeListValue="custodian">custodian</gmd:CI_RoleCode>
					</gmd:role>
				</gmd:CI_ResponsibleParty>
			</gmd:contact>
			<gmd:dateStamp>
				<gco:Date>
					<!--xsl:value-of select="current-date()"/-->
					<!--xsl:value-of select='substring-before(string(current-dateTime()),"T")' /-->
					<xsl:value-of select="date:date()"/>
				</gco:Date>
			</gmd:dateStamp>
			<gmd:metadataStandardName>
				<gco:CharacterString>ISO 19115-2 Geographic Information - Metadata - Part 2: Extensions for Imagery and Gridded Data</gco:CharacterString>
			</gmd:metadataStandardName>
			<gmd:metadataStandardVersion>
				<gco:CharacterString>ISO 19115-2:2009(E)</gco:CharacterString>
			</gmd:metadataStandardVersion>
			<!-- <gmd:dataSetURI>
				<gco:CharacterString>
				String of the data set URI
				</gco:CharacterString>
			</gmd:dataSetURI> -->

			<gmd:spatialRepresentationInfo>
				<xsl:choose>
					<xsl:when test="count($longitudeVariableName) + count($latitudeVariableName) + count($verticalVariableName) + count($timeVariableName)">
						<gmd:MD_GridSpatialRepresentation>
							<gmd:numberOfDimensions>
								<gco:Integer>
									<xsl:value-of select="count($longitudeVariableName)  + count($latitudeVariableName) + count($verticalVariableName)  + count($timeVariableName) "/>
								</gco:Integer>
							</gmd:numberOfDimensions>
							<xsl:if test="count($longitudeVariableName)">
								<xsl:call-template name="writeDimension">
									<xsl:with-param name="dimensionType" select="'column'"/>
									<xsl:with-param name="dimensionUnits" select="$geospatial_lon_units"/>
									<xsl:with-param name="dimensionResolution" select="$geospatial_lon_resolution"/>
									<xsl:with-param name="dimensionSize" select="netcdf/dimension[contains(@name,'lon')]/@length"/>
								</xsl:call-template>
							</xsl:if>
							<xsl:if test="count($latitudeVariableName)">
								<xsl:call-template name="writeDimension">
									<xsl:with-param name="dimensionType" select="'row'"/>
									<xsl:with-param name="dimensionUnits" select="$geospatial_lat_units"/>
									<xsl:with-param name="dimensionResolution" select="$geospatial_lat_resolution"/>
									<xsl:with-param name="dimensionSize" select="netcdf/dimension[contains(@name,'lat')]/@length"/>
								</xsl:call-template>
							</xsl:if>
							<xsl:if test="count($verticalVariableName)">
								<xsl:call-template name="writeDimension">
									<xsl:with-param name="dimensionType" select="'vertical'"/>
									<xsl:with-param name="dimensionUnits" select="$verticalUnits"/>
									<xsl:with-param name="dimensionResolution" select="$verticalResolution"/>
									<xsl:with-param name="dimensionSize" select="netcdf/dimension[contains(@name,$verticalVariableName)]/@length"/>
								</xsl:call-template>
							</xsl:if>
							<xsl:if test="count($timeVariableName)">
								<xsl:call-template name="writeDimension">
									<xsl:with-param name="dimensionType" select="'temporal'"/>
									<xsl:with-param name="dimensionUnits" select="$temporalUnits"/>
									<xsl:with-param name="dimensionResolution" select="$timeResolution"/>
									<xsl:with-param name="dimensionSize" select="netcdf/dimension[contains(@name,$timeVariableName)]/@length"/>
								</xsl:call-template>
							</xsl:if>
							<gmd:cellGeometry>
                 <gmd:MD_CellGeometryCode  codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CellGeometryCode" codeListValue="area"> 
									<xsl:value-of select="'area'"/>
								</gmd:MD_CellGeometryCode>
							</gmd:cellGeometry>
              				<gmd:transformationParameterAvailability>
                     			<gco:Boolean>true</gco:Boolean>
              				</gmd:transformationParameterAvailability>
						</gmd:MD_GridSpatialRepresentation>
					</xsl:when>
					<xsl:otherwise>
						<xsl:attribute name="gco:nilReason">
							<xsl:value-of select="'missing'"/>
						</xsl:attribute>
					</xsl:otherwise>
				</xsl:choose>
			</gmd:spatialRepresentationInfo>

			<gmd:identificationInfo>
				<gmd:MD_DataIdentification id="DataIdentification">
					<gmd:citation>
						<gmd:CI_Citation>
							<gmd:title>
								<xsl:call-template name="writeCharacterString">
									<xsl:with-param name="stringToWrite" select="$englishtitle"/>
								</xsl:call-template>
							</gmd:title>
							<xsl:choose>
								<xsl:when test="$dateCnt">
									<xsl:if test="count($creatorDate)">
										<xsl:call-template name="writeDate">
											<xsl:with-param name="testValue" select="count($creatorDate)"/>
											<xsl:with-param name="dateToWrite" select="substring($creatorDate,0,11)"/>
											<xsl:with-param name="dateType" select="'creation'"/>
										</xsl:call-template>
									</xsl:if>
									<xsl:if test="count($issuedDate)">
										<xsl:call-template name="writeDate">
											<xsl:with-param name="testValue" select="count($issuedDate)"/>
											<xsl:with-param name="dateToWrite" select="$issuedDate[1]"/>
											<xsl:with-param name="dateType" select="'issued'"/>
										</xsl:call-template>
									</xsl:if>
									<xsl:if test="count($modifiedDate)">
										<xsl:call-template name="writeDate">
											<xsl:with-param name="testValue" select="count($modifiedDate)"/>
											<xsl:with-param name="dateToWrite" select="$modifiedDate[1]"/>
											<xsl:with-param name="dateType" select="'revision'"/>
										</xsl:call-template>
									</xsl:if>
								</xsl:when>
								<xsl:otherwise>
									<gmd:date>
										<xsl:attribute name="gco:nilReason">
											<xsl:value-of select="'missing'"/>
										</xsl:attribute>
									</gmd:date>
								</xsl:otherwise>
							</xsl:choose>
							<gmd:identifier>
								<xsl:choose>
									<xsl:when test="count($id)">
										<gmd:MD_Identifier>
											<xsl:if test="$title">
												<gmd:authority>
													<gmd:CI_Citation>
														<gmd:title>
															<gco:CharacterString>
																<xsl:value-of select="$title"/>
															</gco:CharacterString>
														</gmd:title>
														<gmd:date>
															<xsl:attribute name="gco:nilReason"><xsl:value-of select="'inapplicable'"/></xsl:attribute>
														</gmd:date>
													</gmd:CI_Citation>
												</gmd:authority>
											</xsl:if>
											<gmd:code>
												<!--  Just use THREDDs id as it's guaranteed to be unique -->
												<gco:CharacterString>
													<xsl:value-of select="netcdf/group[@name='THREDDSMetadata']/attribute[@name='id']/@value"/>
												</gco:CharacterString>
											</gmd:code>
										</gmd:MD_Identifier>
									</xsl:when>
									<xsl:otherwise>
										<xsl:attribute name="gco:nilReason"><xsl:value-of select="'missing'"/></xsl:attribute>
									</xsl:otherwise>
								</xsl:choose>
							</gmd:identifier>
							<xsl:if test="$creatorTotal">
								<xsl:call-template name="writeResponsibleParty">
									<xsl:with-param name="tagName" select="'gmd:citedResponsibleParty'"/>
									<xsl:with-param name="testValue" select="$creatorTotal"/>
									<xsl:with-param name="individualName" select="$creatorName"/>
									<xsl:with-param name="organisationName" select="$institution"/>
									<xsl:with-param name="email" select="$creatorEmail"/>
									<xsl:with-param name="url" select="$creatorURL"/>
									<xsl:with-param name="roleCode" select="'originator'"/>
								</xsl:call-template>
							</xsl:if>
							<xsl:if test="$contributorTotal">
								<xsl:call-template name="writeResponsibleParty">
									<xsl:with-param name="tagName" select="'gmd:citedResponsibleParty'"/>
									<xsl:with-param name="testValue" select="$contributorTotal"/>
									<xsl:with-param name="individualName" select="$contributorName"/>
									<xsl:with-param name="organisationName" select="'NCEI'"/>
									<xsl:with-param name="email" select="'NCEI.info@noaa.gov'"/>
									<xsl:with-param name="url" select="'http://www.nodc.noaa.gov/SatelliteData/pathfinder4km/'"/>
									<xsl:with-param name="roleCode" select="netcdf/attribute[@name='contributor_role']/@value"/>
								</xsl:call-template>
							</xsl:if>
							<xsl:if test="$comment">
								<gmd:otherCitationDetails>
									<xsl:call-template name="writeCharacterString">
										<xsl:with-param name="stringToWrite" select="$comment[1]"/>
									</xsl:call-template>
								</gmd:otherCitationDetails>
							</xsl:if>
						</gmd:CI_Citation>
					</gmd:citation>
					<gmd:abstract>
						<xsl:call-template name="writeCharacterString">
							<xsl:with-param name="stringToWrite" select="$summary[1]"/>
						</xsl:call-template>
					</gmd:abstract>
					<xsl:if test="count($acknowledgment)">
						<gmd:credit>
							<xsl:call-template name="writeCharacterString">
								<xsl:with-param name="stringToWrite" select="$acknowledgment[1]"/>
							</xsl:call-template>
						</gmd:credit>
					</xsl:if>
					<!-- point of contact is creator -->
					<xsl:call-template name="writeResponsibleParty">
						<xsl:with-param name="tagName" select="'gmd:pointOfContact'"/>
						<xsl:with-param name="testValue" select="$creatorTotal"/>
						<xsl:with-param name="individualName" select="$creatorName"/>
						<xsl:with-param name="organisationName" select="$institution"/>
						<xsl:with-param name="email" select="$creatorEmail"/>
						<xsl:with-param name="url" select="$creatorURL"/>
						<xsl:with-param name="roleCode" select="'pointOfContact'"/>
					</xsl:call-template>

					<xsl:if test="$browsegraphic!=''">
					<gmd:graphicOverview>
						<gmd:MD_BrowseGraphic>
							<gmd:fileName>
								<gco:CharacterString>
									<xsl:value-of select="$browsegraphic"/>
								</gco:CharacterString>
							</gmd:fileName>
							<gmd:fileDescription>
								<gco:CharacterString>Preview graphic</gco:CharacterString>
							</gmd:fileDescription>
							<gmd:fileType>
								<gco:CharacterString>PNG</gco:CharacterString>
							</gmd:fileType>
						</gmd:MD_BrowseGraphic>
					</gmd:graphicOverview>
					</xsl:if>
					
						<xsl:if test="count($keywords)">
						<gmd:descriptiveKeywords>
							<gmd:MD_Keywords>
								<xsl:variable name="keywordDelimiter">
									<xsl:choose>
										<xsl:when test="(contains($keywords,',') or contains($keywords,'&gt;'))">
											<xsl:value-of select="','"/>
										</xsl:when>
										<xsl:otherwise>
											<xsl:value-of select="' '"/>
										</xsl:otherwise>
									</xsl:choose>
								</xsl:variable>
								<xsl:for-each select="str:tokenize($keywords,$keywordDelimiter)">
									<gmd:keyword>
										<gco:CharacterString>
											<xsl:value-of select="."/>
										</gco:CharacterString>
									</gmd:keyword>
								</xsl:for-each>
								<gmd:type>
                 					<gmd:MD_KeywordTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_KeywordTypeCode" codeListValue="theme">
										<xsl:value-of select="'theme'"/>
									</gmd:MD_KeywordTypeCode>
								</gmd:type>
								<gmd:thesaurusName>
									<gmd:CI_Citation>
										<gmd:title>
											<xsl:call-template name="writeCharacterString">
												<xsl:with-param name="stringToWrite" select="$keywordsVocabulary"/>
											</xsl:call-template>
										</gmd:title>
										<gmd:date>
											<xsl:attribute name="gco:nilReason"><xsl:value-of select="'unknown'"/></xsl:attribute>
										</gmd:date>
									</gmd:CI_Citation>
								</gmd:thesaurusName>
							</gmd:MD_Keywords>
						</gmd:descriptiveKeywords>
					</xsl:if>
					
					<gmd:descriptiveKeywords>
						<gmd:MD_Keywords>
							<gmd:keyword>
								<xsl:call-template name="writeCharacterString">
									<xsl:with-param name="stringToWrite" select="substring($fileidentifier, 6, 5)"/>
								</xsl:call-template>
							</gmd:keyword>
							<gmd:type>
								<gmd:MD_KeywordTypeCode codeList="http://www.ngdc.noaa.gov/metadata/published/xsd/schema/resources/Codelist/gmxCodelists.xml#MD_KeywordTypeCode" codeListValue="platform">platform</gmd:MD_KeywordTypeCode>
							</gmd:type>
							<gmd:thesaurusName>
								<gmd:CI_Citation>
									<gmd:title>
										<gco:CharacterString>NODC ENVIRONMENTAL BUOY THESAURUS</gco:CharacterString>
									</gmd:title>
									<gmd:date gco:nilReason="inapplicable"/>
								</gmd:CI_Citation>
							</gmd:thesaurusName>
						</gmd:MD_Keywords>
					</gmd:descriptiveKeywords>
					
					<!-- <gmd:descriptiveKeywords>
						<gmd:MD_Keywords>
							<xsl:for-each select="netcdf/attribute[@name='keywords']">
								<gmd:keyword>
									<gco:CharacterString>
										<xsl:value-of select="./@value[1]"/>
									</gco:CharacterString>
								</gmd:keyword>
							</xsl:for-each>
							<gmd:type>
								<gmd:MD_KeywordTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_KeywordTypeCode" codeListValue="theme">
									<xsl:value-of select="'theme'"/>
								</gmd:MD_KeywordTypeCode>
							</gmd:type>
							<gmd:thesaurusName>
								<gmd:CI_Citation>
									<gmd:title>
										<xsl:choose>
											<xsl:when test="$stdNameVocabulary = 'CF-16.0'">
												<xsl:call-template name="writeCharacterString">
													<xsl:with-param name="stringToWrite" select="'CF-1.6'"/>
												</xsl:call-template>
											</xsl:when>
											<xsl:otherwise>
												<xsl:call-template name="writeCharacterString">
													<xsl:with-param name="stringToWrite" select="$stdNameVocabulary"/>
												</xsl:call-template>
											</xsl:otherwise>
										</xsl:choose>
									</gmd:title>
									<gmd:date gco:nilReason="unknown"/>
								</gmd:CI_Citation>
							</gmd:thesaurusName>
						</gmd:MD_Keywords>
					</gmd:descriptiveKeywords> -->
					
					<!-- <xsl:if test="$standardNameCnt">
						<gmd:descriptiveKeywords>
							<gmd:MD_Keywords>
								<xsl:for-each select="netcdf/variable/attribute[@name='long_name']">
									<gmd:keyword>
										<gco:CharacterString>
											<xsl:value-of select="./@value[1]"/>
										</gco:CharacterString>
									</gmd:keyword>
								</xsl:for-each>
								<gmd:type>
                  <gmd:MD_KeywordTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_KeywordTypeCode" codeListValue="theme">
										<xsl:value-of select="'theme'"/>
									</gmd:MD_KeywordTypeCode>
								</gmd:type>
								<gmd:thesaurusName>
									<gmd:CI_Citation>
										<gmd:title>
											<xsl:call-template name="writeCharacterString">
												<xsl:with-param name="stringToWrite" select="$stdNameVocabulary[1]"/>
											</xsl:call-template>
										</gmd:title>
										<gmd:date gco:nilReason="unknown"/>
									</gmd:CI_Citation>
								</gmd:thesaurusName>
							</gmd:MD_Keywords>
						</gmd:descriptiveKeywords>
					</xsl:if> -->
					
					<xsl:if test="count($license)">
						<gmd:resourceConstraints>
							<gmd:MD_LegalConstraints>
								<gmd:useLimitation>
									<gco:CharacterString>
										<xsl:value-of select="$license[1]"/>
									</gco:CharacterString>
								</gmd:useLimitation>
							</gmd:MD_LegalConstraints>
						</gmd:resourceConstraints>
					</xsl:if>
					<gmd:resourceConstraints>
					    <gmd:MD_LegalConstraints>
					        <gmd:useConstraints>
					            <gmd:MD_RestrictionCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_RestrictionCode" codeListValue="otherRestrictions" codeSpace="008">other Restrictions</gmd:MD_RestrictionCode>
					        </gmd:useConstraints>
					        <gmd:otherConstraints>
					            <gco:CharacterString>Use liability: NOAA and NCEI cannot provide any warranty as to the accuracy, reliability, or completeness of furnished data. Users assume responsibility to determine the usability of these data. The user is responsible for the results of any application of this data for other than its intended purpose.</gco:CharacterString>
					        </gmd:otherConstraints>
					    </gmd:MD_LegalConstraints>
					</gmd:resourceConstraints>
					<gmd:resourceConstraints>
					    <gmd:MD_LegalConstraints>
					        <gmd:accessConstraints>
					            <gmd:MD_RestrictionCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_RestrictionCode" codeListValue="otherRestrictions" codeSpace="008">other Restrictions</gmd:MD_RestrictionCode>
					        </gmd:accessConstraints>
					        <gmd:otherConstraints>
					            <gco:CharacterString>Distribution liability: NOAA and NCEI make no warranty, expressed or implied, regarding these data, nor does the fact of distribution constitute such a warranty. NOAA and NCEI cannot assume liability for any damages caused by any errors or omissions in these data. If appropriate, NCEI can only certify that the data it distributes are an authentic copy of the records that were accepted for inclusion in the NCEI archives.</gco:CharacterString>
					        </gmd:otherConstraints>
					    </gmd:MD_LegalConstraints>
					</gmd:resourceConstraints>
					<gmd:language>
						<gco:CharacterString>eng; USA</gco:CharacterString>
					</gmd:language>
					<gmd:topicCategory>
						<gmd:MD_TopicCategoryCode>climatologyMeteorologyAtmosphere</gmd:MD_TopicCategoryCode>
					</gmd:topicCategory>
					<gmd:extent>
						<xsl:choose>
							<xsl:when test="$extentTotal">
								<gmd:EX_Extent>
									<xsl:attribute name="id"><xsl:value-of select="'boundingExtent'"/></xsl:attribute>
									<xsl:if test="'1'">
										<gmd:geographicElement>
											<gmd:EX_GeographicBoundingBox id="boundingGeographicBoundingBox">
												<gmd:extentTypeCode>
													<gco:Boolean>1</gco:Boolean>
												</gmd:extentTypeCode>
												<gmd:westBoundLongitude>
													<gco:Decimal>
														<xsl:value-of select="$geospatial_lon_min"/>
													</gco:Decimal>
												</gmd:westBoundLongitude>
												<gmd:eastBoundLongitude>
													<gco:Decimal>
														<xsl:value-of select="$geospatial_lon_max"/>
													</gco:Decimal>
												</gmd:eastBoundLongitude>
												<gmd:southBoundLatitude>
													<gco:Decimal>
														<xsl:value-of select="$geospatial_lat_min"/>
													</gco:Decimal>
												</gmd:southBoundLatitude>
												<gmd:northBoundLatitude>
													<gco:Decimal>
														<xsl:value-of select="$geospatial_lat_max"/>
													</gco:Decimal>
												</gmd:northBoundLatitude>
											</gmd:EX_GeographicBoundingBox>
										</gmd:geographicElement>
									</xsl:if>
									<xsl:if test="count($timeStart) + count($timeEnd)">
										<gmd:temporalElement>
											<gmd:EX_TemporalExtent>
												<xsl:attribute name="id">
													<xsl:value-of select="'boundingTemporalExtent'"/>
												</xsl:attribute>
												<gmd:extent>
													<gml:TimePeriod gml:id="{generate-id()}">
														<gml:description>
															<xsl:value-of select="$temporalUnits"/>
														</gml:description>
														<gml:beginPosition>
															<xsl:value-of select="substring($timeStart,0,11)"/>
														</gml:beginPosition>
														<gml:endPosition>
															<xsl:value-of select="substring($timeEnd,0,11)"/>
														</gml:endPosition>
													</gml:TimePeriod>
												</gmd:extent>
											</gmd:EX_TemporalExtent>
										</gmd:temporalElement>
									</xsl:if>
									
								</gmd:EX_Extent>
							</xsl:when>


							<xsl:otherwise>
								<gmd:EX_Extent>
									<gmd:geographicElement>
										<gmd:EX_GeographicBoundingBox>
											<gmd:extentTypeCode>
												<gco:Boolean>1</gco:Boolean>
											</gmd:extentTypeCode>
											<gmd:westBoundLongitude>
												<gco:Decimal>-180.</gco:Decimal>
											</gmd:westBoundLongitude>
											<gmd:eastBoundLongitude>
												<gco:Decimal>180.</gco:Decimal>
											</gmd:eastBoundLongitude>
											<gmd:southBoundLatitude>
												<gco:Decimal>-90.</gco:Decimal>
											</gmd:southBoundLatitude>
											<gmd:northBoundLatitude>
												<gco:Decimal>90.</gco:Decimal>
											</gmd:northBoundLatitude>
										</gmd:EX_GeographicBoundingBox>
									</gmd:geographicElement>
									<gmd:temporalElement>
										<gmd:EX_TemporalExtent>
											<xsl:attribute name="id">
												<xsl:value-of select="'boundingTemporalExtent'"/>
											</xsl:attribute>
											<gmd:extent>
												<gml:TimePeriod gml:id="{generate-id()}">
													<gml:description>
														<xsl:value-of select="$temporalUnits"/>
														<xsl:value-of select="'UTC'"/>
													</gml:description>
													<gml:beginPosition>
														<xsl:value-of select="substring($timeStart, 0, 11)"/>
													</gml:beginPosition>
													<gml:endPosition>
														<xsl:value-of select="substring($timeEnd, 0,11)"/>
													</gml:endPosition>
												</gml:TimePeriod>
											</gmd:extent>
										</gmd:EX_TemporalExtent>
									</gmd:temporalElement>
									
								</gmd:EX_Extent>
							</xsl:otherwise>
						</xsl:choose>
					</gmd:extent>
				</gmd:MD_DataIdentification>
			</gmd:identificationInfo>

			<!-- <xsl:if test="$Pathfinderhttp">
				<xsl:call-template name="writeService">
					<xsl:with-param name="serviceID" select="'HTTP_SERVER'"/>
					<xsl:with-param name="serviceTypeName" select="'HTTP'"/>
					<xsl:with-param name="serviceOperationName" select="'HTTP Client Access'"/>
					<xsl:with-param name="operationURL" select="$Pathfinderhttp"/>
				</xsl:call-template>
			</xsl:if>

			<xsl:if test="'1'">
				<xsl:call-template name="writeService">
					<xsl:with-param name="serviceID" select="'FTP'"/>
					<xsl:with-param name="serviceTypeName" select="'FTP'"/>
					<xsl:with-param name="serviceOperationName" select="'FTP Client Access'"/>
					<xsl:with-param name="operationURL" select="$Pathfinderftp"/>
				</xsl:call-template>
			</xsl:if>
			<xsl:if test="$Pathfinderthredds">
				<xsl:call-template name="writeService">
					<xsl:with-param name="serviceID" select="'THREDDS'"/>
					<xsl:with-param name="serviceTypeName" select="'THREDDS DATA SERVER'"/>
					<xsl:with-param name="serviceOperationName" select="'THREDDS Client Access'"/>
					<xsl:with-param name="operationURL" select="$Pathfinderthredds"/></xsl:call-template>
			</xsl:if> -->
	
				<!-- WMS -->
			        <xsl:call-template name="writeService">
			          <xsl:with-param name="serviceID" select="'OGC_WMS'"/>
			          <xsl:with-param name="serviceTypeName" select="'Open Geospatial Consortium Web Map Service (WMS)'"/>
			          <xsl:with-param name="serviceOperationName" select="'GetCapabilities'"/>
			        	<xsl:with-param name="operationURL" select="translate(normalize-space(concat('http://data.nodc.noaa.gov/thredds/wms/', netcdf/path, netcdf/title,'.nc?service=WMS&amp;version=1.3.0&amp;request=GetCapabilities')),' ','')"/>
			        </xsl:call-template>
			      
			     <!-- WCS -->
			        <xsl:call-template name="writeService">
			          <xsl:with-param name="serviceID" select="'OGC_WCS'"/>
			          <xsl:with-param name="serviceTypeName" select="'Open Geospatial Consortium Web Content Service (WCS)'"/>
			          <xsl:with-param name="serviceOperationName" select="'GetCapabilities'"/>
			        	<xsl:with-param name="operationURL" select="translate(normalize-space(concat('http://data.nodc.noaa.gov/thredds/wcs/', netcdf/path, netcdf/title,'.nc?service=WCS&amp;version=1.0.0&amp;request=GetCapabilities')),' ','')"/>
			        </xsl:call-template>
			     
			      <xsl:if test="subsetcount">
			        <xsl:call-template name="writeService">
			          <xsl:with-param name="serviceID" select="'THREDDS_NetCDF_Subset'"/>
			          <xsl:with-param name="serviceTypeName" select="'THREDDS NetCDF Subset Service'"/>
			          <xsl:with-param name="serviceOperationName" select="'NetCDFSubsetService'"/>
			          <xsl:with-param name="operationURL" select="$thredds_netcdfsubsetCnt"/>
			        </xsl:call-template>
			      </xsl:if>

			    <xsl:if test="$physicalMeasurementCnt">
				<gmd:contentInfo>
					<gmi:MI_CoverageDescription>
						<gmd:attributeDescription>
							<xsl:attribute name="gco:nilReason"><xsl:value-of select="'unknown'"/></xsl:attribute>
						</gmd:attributeDescription>
						<gmd:contentType>
              				<gmd:MD_CoverageContentTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CoverageContentTypeCode" codeListValue="physicalMeasurement">
								<xsl:value-of select="'physicalMeasurement'"/>
							</gmd:MD_CoverageContentTypeCode>
						</gmd:contentType>
						<xsl:for-each select="netcdf/variable[not(contains((translate(@name,ABCDEFGHIJKLMNOPQRSTUVWXYZ,abcdefghijklmnopqrstuvwxyz)),'_qc'))]">
							<xsl:if test="@name != @shape">
								<xsl:call-template name="writeVariableDimensions">
									<xsl:with-param name="variableName" select="./@name"/>
									<xsl:with-param name="variableLongName" select="./attribute[@name='long_name']/@value"/>
									<xsl:with-param name="variableStandardName" select="./attribute[@name='standard_name']/@value"/>
									<xsl:with-param name="variableType" select="./@type"/>
									<xsl:with-param name="variableUnits" select="./attribute[@name='units']/@value"/>
								</xsl:call-template>
							</xsl:if>
						</xsl:for-each>
						<xsl:for-each select="netcdf/variable[not(contains((translate(@name,ABCDEFGHIJKLMNOPQRSTUVWXYZ,abcdefghijklmnopqrstuvwxyz)),'_qc'))]">
							<xsl:if test="@name != @shape">
								<xsl:call-template name="writeVariableRanges">
									<xsl:with-param name="variableName" select="./@name"/>
									<xsl:with-param name="variableLongName" select="./attribute[@name='long_name']/@value"/>
									<xsl:with-param name="variableStandardName" select="./attribute[@name='standard_name']/@value"/>
									<xsl:with-param name="variableType" select="./@type"/>
									<xsl:with-param name="variableUnits" select="./attribute[@name='units']/@value"/>
								</xsl:call-template>
							</xsl:if>
						</xsl:for-each>
					</gmi:MI_CoverageDescription>
				</gmd:contentInfo>
			</xsl:if>
			<xsl:if test="$qualityInformationCnt">
				<gmd:contentInfo>
					<gmi:MI_CoverageDescription>
						<gmd:attributeDescription>
							<xsl:attribute name="gco:nilReason"><xsl:value-of select="'unknown'"/></xsl:attribute>
						</gmd:attributeDescription>




						<gmd:contentType>
          				    <gmd:MD_CoverageContentTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CoverageContentTypeCode" codeListValue="qualityInformation">
								<xsl:value-of select="'qualityInformation'"/>
							</gmd:MD_CoverageContentTypeCode>
						</gmd:contentType>
						<xsl:for-each select="netcdf/variable[not(contains((translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')),'_qc'))]">
							<xsl:if test="@name != @shape">
								<xsl:call-template name="writeVariableDimensions">
									<xsl:with-param name="variableName" select="./@name"/>
									<xsl:with-param name="variableLongName" select="./attribute[@name='long_name']/@value"/>
									<xsl:with-param name="variableStandardName" select="./attribute[@name='standard_name']/@value"/>
									<xsl:with-param name="variableType" select="./@type"/>
									<xsl:with-param name="variableUnits" select="./attribute[@name='units']/@value"/>
								</xsl:call-template>
							</xsl:if>
						</xsl:for-each>
						<xsl:for-each select="netcdf/variable[not(contains((translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')),'_qc'))]">
							<xsl:if test="@name != @shape">
								<xsl:call-template name="writeVariableRanges">
									<xsl:with-param name="variableName" select="./@name"/>
									<xsl:with-param name="variableLongName" select="./attribute[@name='long_name']/@value"/>
									<xsl:with-param name="variableStandardName" select="./attribute[@name='standard_name']/@value"/>
									<xsl:with-param name="variableType" select="./@type"/>
									<xsl:with-param name="variableUnits" select="./attribute[@name='units']/@value"/>
								</xsl:call-template>
							</xsl:if>
						</xsl:for-each>
					</gmi:MI_CoverageDescription>
				</gmd:contentInfo>
			</xsl:if>
			<!-- distributor is netCDF publisher -->
			<xsl:if test="$serviceMax">
				<gmd:distributionInfo>
					<gmd:MD_Distribution>
						<gmd:distributor>
							<gmd:MD_Distributor>
								<xsl:choose>
									<xsl:when test="$publisherTotal">
										<xsl:call-template name="writeResponsibleParty">
											<xsl:with-param name="tagName" select="'gmd:distributorContact'"/>
											<xsl:with-param name="testValue" select="$publisherTotal"/>
											<xsl:with-param name="individualName"/>
											<xsl:with-param name="organisationName" select="$publisherName"/>
											<xsl:with-param name="email" select="$publisherEmail"/>
											<xsl:with-param name="url" select="$publisherURL"/>
											<xsl:with-param name="urlName" select="'URL for the data publisher'"/>
											<xsl:with-param name="urlDescription" select="'This URL provides contact information for the publisher of this dataset'"/>
											<xsl:with-param name="roleCode" select="'publisher'"/>
										</xsl:call-template>
									</xsl:when>
									<xsl:otherwise>
										<gmd:distributorContact gco:nilReason="missing"/>
									</xsl:otherwise>
								</xsl:choose>
								<gmd:distributorFormat>
									<gmd:MD_Format>
										<gmd:name>
											<gco:CharacterString>NetCDF</gco:CharacterString>
										</gmd:name>
										<gmd:version gco:nilReason="unknown"/>
									</gmd:MD_Format>
								</gmd:distributorFormat>
								<xsl:if test="$Pathfinderhttp">
									<gmd:distributorTransferOptions>
										<gmd:MD_DigitalTransferOptions>
											<gmd:transferSize>
												<gco:Real><xsl:value-of select="$filesize"/></gco:Real>
											</gmd:transferSize>
											<gmd:onLine>
												<gmd:CI_OnlineResource>
													<gmd:linkage>
														<gmd:URL>
															<xsl:value-of select="translate($Pathfinderhttp,' ','')"/>
														</gmd:URL>
													</gmd:linkage>
													<gmd:protocol>
														<gco:CharacterString>HTTP</gco:CharacterString>
													</gmd:protocol>
													<gmd:name>
														<gco:CharacterString>HTTP</gco:CharacterString>
													</gmd:name>
													<gmd:description>
														<gco:CharacterString>This URL provides a standard HTTP interface for selecting data from this dataset. The transfer size is in kb.</gco:CharacterString>
													</gmd:description>
													<gmd:function>
														<gmd:CI_OnLineFunctionCode codeList= "http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_OnLineFunctionCode" codeListValue="download">download</gmd:CI_OnLineFunctionCode>
													</gmd:function>
												</gmd:CI_OnlineResource>
											</gmd:onLine>
										</gmd:MD_DigitalTransferOptions>
									</gmd:distributorTransferOptions>
								</xsl:if>
								<xsl:if test="$Pathfinderftp">
									<gmd:distributorTransferOptions>
										<gmd:MD_DigitalTransferOptions>
											<gmd:transferSize>
												<gco:Real><xsl:value-of select="$filesize"/></gco:Real>
											</gmd:transferSize>
											<gmd:onLine>
												<gmd:CI_OnlineResource>
													<gmd:linkage>
														<gmd:URL>
															<xsl:value-of select="translate($Pathfinderftp,' ','')" />
														</gmd:URL>
													</gmd:linkage>
													<gmd:protocol>
														<gco:CharacterString>FTP</gco:CharacterString>
													</gmd:protocol>
													<gmd:name>
														<gco:CharacterString>FTP</gco:CharacterString>
													</gmd:name>
													<gmd:description>
														<gco:CharacterString>This URL provides a standard FTP interface for selecting data from this dataset. The transfer size is in kb.</gco:CharacterString>
													</gmd:description>
													<gmd:function>
														<gmd:CI_OnLineFunctionCode codeList= "http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_OnLineFunctionCode" codeListValue="download">download</gmd:CI_OnLineFunctionCode>
													</gmd:function>
												</gmd:CI_OnlineResource>
											</gmd:onLine>
										</gmd:MD_DigitalTransferOptions>
									</gmd:distributorTransferOptions>
								</xsl:if>
								<xsl:if test="$Pathfinderthredds">
									<gmd:distributorTransferOptions>
										<gmd:MD_DigitalTransferOptions>
											<gmd:transferSize>
												<gco:Real><xsl:value-of select="$filesize"/></gco:Real>
											</gmd:transferSize>
											<gmd:onLine>
												<gmd:CI_OnlineResource>
													<gmd:linkage>
														<gmd:URL>
															<xsl:value-of select="translate($Pathfinderthredds,' ', '')" />
														</gmd:URL>
													</gmd:linkage>
													<gmd:protocol>
														<gco:CharacterString>UNIDATA:THREDDS</gco:CharacterString>
													</gmd:protocol>
													<gmd:name>
														<gco:CharacterString>THREDDS(TDS)</gco:CharacterString>
													</gmd:name>
													<gmd:description>
														<gco:CharacterString>This URL provides a standard HTTP interface for selecting data from this dataset. The transfer size is in kb.</gco:CharacterString>
													</gmd:description>
													<gmd:function>
														<gmd:CI_OnLineFunctionCode codeList= "http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_OnLineFunctionCode" codeListValue="download">download</gmd:CI_OnLineFunctionCode>
													</gmd:function>
												</gmd:CI_OnlineResource>
											</gmd:onLine>
										</gmd:MD_DigitalTransferOptions>
									</gmd:distributorTransferOptions>
								</xsl:if>
								<xsl:if test="$Pathfinderopendap">
									<gmd:distributorTransferOptions>
										<gmd:MD_DigitalTransferOptions>
											<gmd:transferSize>
												<gco:Real><xsl:value-of select="$filesize"/></gco:Real>
											</gmd:transferSize>
											<gmd:onLine>
												<gmd:CI_OnlineResource>
													<gmd:linkage>
														<gmd:URL>
															<xsl:value-of select="translate($Pathfinderopendap,' ','')"/>
														</gmd:URL>
													</gmd:linkage>
													<gmd:protocol>
														<gco:CharacterString>OPeNDAP:Hyrax</gco:CharacterString>
													</gmd:protocol>
													<gmd:name>
														<gco:CharacterString>THREDDS OPeNDAP</gco:CharacterString>
													</gmd:name>
													<gmd:description>
														<gco:CharacterString>This URL provides a standard HTTP interface for selecting data from this dataset. The transfer size is in kb.</gco:CharacterString>
													</gmd:description>
													<gmd:function>
                           								 <gmd:CI_OnLineFunctionCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_OnLineFunctionCode" codeListValue="download">download</gmd:CI_OnLineFunctionCode>
													</gmd:function>
												</gmd:CI_OnlineResource>
											</gmd:onLine>
										</gmd:MD_DigitalTransferOptions>
									</gmd:distributorTransferOptions>
								</xsl:if>
							</gmd:MD_Distributor>
						</gmd:distributor>
					</gmd:MD_Distribution>
				</gmd:distributionInfo>
			</xsl:if>
			<xsl:if test="normalize-space($history[1])!=''">
				<gmd:dataQualityInfo>
					<gmd:DQ_DataQuality>
						<gmd:scope>
							<gmd:DQ_Scope>
								<gmd:level>
                  <gmd:MD_ScopeCode  codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ScopeCode" codeListValue="dataset">
										<xsl:value-of select="'dataset'"/>
									</gmd:MD_ScopeCode>
								</gmd:level>
							</gmd:DQ_Scope>
						</gmd:scope>
						<gmd:lineage>
							<gmd:LI_Lineage>
								<gmd:statement>
									<xsl:call-template name="writeCharacterString">
										<xsl:with-param name="stringToWrite" select="$history[1]"/>
									</xsl:call-template>
								</gmd:statement>
							</gmd:LI_Lineage>
						</gmd:lineage>
					</gmd:DQ_DataQuality>
				</gmd:dataQualityInfo>
			</xsl:if>
		</gmi:MI_Metadata>
	</xsl:template>
	<xsl:template name="writeCodelist">
		<xsl:param name="codeListName"/>
		<xsl:param name="codeListValue"/>
		<xsl:variable name="codeListLocation" select="'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml'"/>
		<xsl:element name="{$codeListName}">
			<xsl:attribute name="codeList">
				<xsl:value-of select="$codeListLocation"/>
				<xsl:value-of select="'#'"/>
				<xsl:value-of select="$codeListName"/>
				</xsl:attribute>
			<xsl:attribute name="codeListValue">
				<xsl:value-of select="$codeListValue"/>
				</xsl:attribute>
			<xsl:value-of select="$codeListValue"/>
		</xsl:element>
	</xsl:template>
	<xsl:template name="writeCharacterString">
		<xsl:param name="stringToWrite"/>
		<xsl:choose>
			<xsl:when test="$stringToWrite">
				<gco:CharacterString>
					<xsl:value-of select="$stringToWrite"/>
				</gco:CharacterString>
			</xsl:when>
			<xsl:otherwise>
				<xsl:attribute name="gco:nilReason"><xsl:value-of select="'missing'"/></xsl:attribute>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="writeDate">
		<xsl:param name="testValue"/>
		<xsl:param name="dateToWrite"/>
		<xsl:param name="dateType"/>
		<xsl:if test="$testValue">
			<xsl:choose>
				<xsl:when test="contains(translate($dateToWrite,' ','T'), 'T' ) ">
					<gmd:date>
						<gmd:CI_Date>
							<gmd:date>
								<gco:Date>
									<xsl:if test="$dateToWrite=''">
										<xsl:value-of select="date:date()"/>
									</xsl:if>
									<xsl:value-of select="substring(translate($dateToWrite,' ','T'),0,11)"/>
								</gco:Date>
							</gmd:date>
							<gmd:dateType>
								<gmd:CI_DateTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode" codeListValue="$dateType">
									<xsl:value-of select="$dateType"/>
								</gmd:CI_DateTypeCode>
							</gmd:dateType>
						</gmd:CI_Date>
					</gmd:date>
				</xsl:when>
				<xsl:otherwise>
					<gmd:date>
						<gmd:CI_Date>
							<gmd:date>
								<gco:Date>
									<xsl:if test="$dateToWrite=''">
										<xsl:value-of select="date:date()"/>
									</xsl:if>
									<xsl:value-of select="substring(translate($dateToWrite,' ','T'),0,11)"/>
								</gco:Date>
							</gmd:date>
							<gmd:dateType>
								<gmd:CI_DateTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode" codeListValue="$dateType">
									<xsl:value-of select="$dateType"/>
								</gmd:CI_DateTypeCode>
							</gmd:dateType>
						</gmd:CI_Date>
					</gmd:date>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>

<!-- "writeResponsibleParty" template definition -->
	<xsl:template name="writeResponsibleParty">
		<xsl:param name="tagName"/>
		<xsl:param name="testValue"/>
		<xsl:param name="individualName"/>
		<xsl:param name="organisationName"/>
		<xsl:param name="email"/>
		<xsl:param name="url"/>
		<xsl:param name="urlName"/>
		<xsl:param name="urlDescription"/>
		<xsl:param name="roleCode"/>
		<xsl:choose>
			<xsl:when test="$testValue">
				<xsl:element name="{$tagName}">
					<gmd:CI_ResponsibleParty>
						<gmd:organisationName>
							<xsl:call-template name="writeCharacterString">
								<xsl:with-param name="stringToWrite" select="$organisationName"/>
							</xsl:call-template>
						</gmd:organisationName>
						<gmd:contactInfo>
							<xsl:choose>
								<xsl:when test="$email or $url">
									<gmd:CI_Contact>
										<xsl:if test="$email">
											<gmd:address>
												<gmd:CI_Address>
													<gmd:electronicMailAddress>
														<gco:CharacterString>
															<xsl:value-of select="$email"/>
														</gco:CharacterString>
													</gmd:electronicMailAddress>
												</gmd:CI_Address>
											</gmd:address>
										</xsl:if>
									<!--	<xsl:if test="$url">
											<gmd:onlineResource>
												<gmd:CI_OnlineResource>
													<gmd:linkage>
														<gmd:URL>
															<xsl:value-of select="$url"/>
														</gmd:URL>
													</gmd:linkage>
													<gmd:protocol>
														<gco:CharacterString>http</gco:CharacterString>
													</gmd:protocol>
													<gmd:applicationProfile>
														<gco:CharacterString>web browser</gco:CharacterString>
													</gmd:applicationProfile>
													<gmd:name>
														<gco:CharacterString>File Information</gco:CharacterString>
													</gmd:name>
													<gmd:description>
														<gco:CharacterString>This URL provides a standard HTTP interface for selecting data from this dataset.</gco:CharacterString>
													</gmd:description>
													<gmd:function>
														<gmd:CI_OnLineFunctionCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_OnLineFunctionCode" codeListValue="information">
															<xsl:value-of select="'information'"/>
														</gmd:CI_OnLineFunctionCode>
													</gmd:function>
												</gmd:CI_OnlineResource>
											</gmd:onlineResource>
										</xsl:if>
									-->	
									</gmd:CI_Contact>
								</xsl:when>
								<xsl:otherwise>
									<xsl:attribute name="gco:nilReason"><xsl:value-of select="'missing'"/></xsl:attribute>
								</xsl:otherwise>
							</xsl:choose>
						</gmd:contactInfo>
						<gmd:role>
							<gmd:CI_RoleCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode" codeListValue="$roleCode">
								<xsl:value-of select="$roleCode"/>
							</gmd:CI_RoleCode>
						</gmd:role>
					</gmd:CI_ResponsibleParty>
				</xsl:element>
			</xsl:when>
			<xsl:otherwise>
				<gmd:contact>
<gmd:CI_ResponsibleParty>
<gmd:organisationName>
<gco:CharacterString>
DOC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce
</gco:CharacterString>
</gmd:organisationName>
<gmd:positionName>
<gco:CharacterString>Data Officer</gco:CharacterString>
</gmd:positionName>
<gmd:contactInfo>
<gmd:CI_Contact>
<gmd:phone>
<gmd:CI_Telephone>
<gmd:voice>
<gco:CharacterString>301-713-3277</gco:CharacterString>
</gmd:voice>
<gmd:facsimile>
<gco:CharacterString>301-713-3300</gco:CharacterString>
</gmd:facsimile>
</gmd:CI_Telephone>
</gmd:phone>
<gmd:address>
<gmd:CI_Address>
<gmd:deliveryPoint>
<gco:CharacterString>Federal Building 151 Patton Avenue</gco:CharacterString>
</gmd:deliveryPoint>
<gmd:city>
<gco:CharacterString>Asheville</gco:CharacterString>
</gmd:city>
<gmd:administrativeArea>
<gco:CharacterString>NC</gco:CharacterString>
</gmd:administrativeArea>
<gmd:postalCode>
<gco:CharacterString>28801-5001</gco:CharacterString>
</gmd:postalCode>
<gmd:country>
<gco:CharacterString>USA</gco:CharacterString>
</gmd:country>
<gmd:electronicMailAddress>
<gco:CharacterString>NCEI.info@noaa.gov</gco:CharacterString>
</gmd:electronicMailAddress>
</gmd:CI_Address>
</gmd:address>
<gmd:onlineResource>
<gmd:CI_OnlineResource>
<gmd:linkage>
<gmd:URL>https://www.ncei.noaa.gov/</gmd:URL>
</gmd:linkage>
<gmd:protocol>
<gco:CharacterString>HTTP</gco:CharacterString>
</gmd:protocol>
<gmd:applicationProfile>
<gco:CharacterString>Standard Internet browser</gco:CharacterString>
</gmd:applicationProfile>
<gmd:name>
<gco:CharacterString>
NOAA National Centers for Environmental Information website
</gco:CharacterString>
</gmd:name>
<gmd:description>
<gco:CharacterString>
Main NCEI website providing links to access data and data services.
</gco:CharacterString>
</gmd:description>
<gmd:function>
<gmd:CI_OnLineFunctionCode codeList="http://www.ngdc.noaa.gov/metadata/published/xsd/schema/resources/Codelist/gmxCodelists.xml#CI_OnLineFunctionCode" codeListValue="information">information</gmd:CI_OnLineFunctionCode>
</gmd:function>
</gmd:CI_OnlineResource>
</gmd:onlineResource>
</gmd:CI_Contact>
</gmd:contactInfo>
<gmd:role>
<gmd:CI_RoleCode codeList="http://www.ngdc.noaa.gov/metadata/published/xsd/schema/resources/Codelist/gmxCodelists.xml#CI_RoleCode" codeListValue="custodian">custodian</gmd:CI_RoleCode>
</gmd:role>
</gmd:CI_ResponsibleParty>
</gmd:contact>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template name="writeDimension">
		<xsl:param name="dimensionName"/>
		<xsl:param name="dimensionType"/>
		<xsl:param name="dimensionUnits"/>
		<xsl:param name="dimensionResolution"/>
		<xsl:param name="dimensionSize"/>
		<gmd:axisDimensionProperties>
			<gmd:MD_Dimension>
				<xsl:if test="$dimensionName">
					<xsl:attribute name="id"><xsl:value-of select="$dimensionName"/></xsl:attribute>
				</xsl:if>
				<gmd:dimensionName>
					<gmd:MD_DimensionNameTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_DimensionNameTypeCode" codeListValue="$dimensionType">
						<xsl:value-of select="$dimensionType"/>
					</gmd:MD_DimensionNameTypeCode>
				</gmd:dimensionName>
				<xsl:choose>
					<xsl:when test="$dimensionSize">
						<gmd:dimensionSize>
							<gco:Integer>
								<xsl:value-of select="$dimensionSize"/>
							</gco:Integer>
						</gmd:dimensionSize>
					</xsl:when>
					<xsl:otherwise>
						<gmd:dimensionSize>
							<xsl:attribute name="gco:nilReason"><xsl:value-of select="'unknown'"/></xsl:attribute>
						</gmd:dimensionSize>
					</xsl:otherwise>
				</xsl:choose>
				<gmd:resolution>
					<xsl:choose>
						<xsl:when test="contains($dimensionResolution,' ')">
							<gco:Measure>
								<xsl:attribute name="uom"><xsl:value-of select="substring-after($dimensionResolution,' ')"/></xsl:attribute>
								<xsl:value-of select="substring-before($dimensionResolution,' ')"/>
							</gco:Measure>
						</xsl:when>
						<xsl:when test="contains($dimensionResolution,'PT')">
							<gco:Measure>
								<xsl:attribute name="uom"><xsl:if test="substring($dimensionResolution, 4)='S'"><xsl:value-of select="translate(substring($dimensionResolution, 4),$uppercase, $smallcase)"/></xsl:if><xsl:if test="substring($dimensionResolution, 4)='M'">minutes</xsl:if></xsl:attribute>
								<xsl:value-of select="substring($dimensionResolution,3,1)"/>
							</gco:Measure>
						</xsl:when>
						<!-- <xsl:when test="$dimensionUnits and $dimensionResolution">
							<gco:Measure>
								<xsl:attribute name="uom"><xsl:value-of select="$dimensionUnits"/></xsl:attribute>
								<xsl:value-of select="$dimensionResolution"/>
							</gco:Measure>	
						</xsl:when> -->
						<xsl:when test="$dimensionUnits and not($dimensionResolution)">
							<xsl:attribute name="gco:nilReason">missing</xsl:attribute>
						</xsl:when>
						<xsl:when test="not($dimensionUnits) and $dimensionResolution">
							<gco:Measure>
								<xsl:attribute name="uom"><xsl:value-of select="'unknown'"/></xsl:attribute>
								<xsl:value-of select="$dimensionResolution"/>
							</gco:Measure>
						</xsl:when>
						<xsl:otherwise>
							<xsl:attribute name="gco:nilReason"><xsl:value-of select="'missing'"/></xsl:attribute>
						</xsl:otherwise>
					</xsl:choose>
				</gmd:resolution>
			</gmd:MD_Dimension>
		</gmd:axisDimensionProperties>
	</xsl:template>
	<xsl:template name="writeVariableDimensions">
		<xsl:param name="variableName"/>
		<xsl:param name="variableLongName"/>
		<xsl:param name="variableStandardName"/>
		<xsl:param name="variableType"/>
		<xsl:param name="variableUnits"/>
		<gmd:dimension>
			<gmd:MD_Band>
				<gmd:sequenceIdentifier>
					<gco:MemberName>
						<gco:aName>
							<gco:CharacterString>
								<xsl:value-of select="$variableName"/>
							</gco:CharacterString>
						</gco:aName>
						<gco:attributeType>
							<gco:TypeName>
								<gco:aName>
									<gco:CharacterString>
										<xsl:value-of select="$variableType"/>
									</gco:CharacterString>
								</gco:aName>
							</gco:TypeName>
						</gco:attributeType>
					</gco:MemberName>
				</gmd:sequenceIdentifier>
				<gmd:descriptor>
					<xsl:call-template name="writeCharacterString">
						<xsl:with-param name="stringToWrite">
							<xsl:value-of select="$variableLongName"/>
							<xsl:if test="$variableStandardName">
								<xsl:value-of select="concat(' (',$variableStandardName,')')"/>
							</xsl:if>
						</xsl:with-param>
					</xsl:call-template>
				</gmd:descriptor>
				<!-- <gmd:units>
					<xsl:attribute name="xlink:href"><xsl:value-of select="'http://someUnitsDictionary.xml#'"/><xsl:value-of select="$variableUnits"/></xsl:attribute> 
				</gmd:units> -->
			</gmd:MD_Band>
		</gmd:dimension>
	</xsl:template>
	<xsl:template name="writeVariableRanges">
		<xsl:param name="variableName"/>
		<xsl:param name="variableLongName"/>
		<xsl:param name="variableStandardName"/>
		<xsl:param name="variableType"/>
		<xsl:param name="variableUnits"/>
		<xsl:if test="attribute[contains(@name,'flag_')]">
			<xsl:variable name="flag_masks_seq" select="str:tokenize(normalize-space(attribute[@name='flag_masks']/@value),' ')"/>
			<xsl:variable name="flag_values_seq" select="str:tokenize(normalize-space(attribute[@name='flag_values']/@value),' ')"/>
			<xsl:variable name="flag_names_seq" select="str:tokenize(normalize-space(attribute[@name='flag_names']/@value),' ')"/>
			<xsl:variable name="flag_meanings_seq" select="str:tokenize(normalize-space(attribute[@name='flag_meanings']/@value),' ')"/>
		</xsl:if>
	</xsl:template>
	<xsl:template name="writeService">
		<xsl:param name="serviceID"/>
		<xsl:param name="serviceTypeName"/>
		<xsl:param name="serviceOperationName"/>
		<xsl:param name="operationURL"/>
		<xsl:param name="operationNode"/>
		<gmd:identificationInfo>
			<xsl:element name="srv:SV_ServiceIdentification">
				<xsl:attribute name="id"><xsl:value-of select="$serviceID"/></xsl:attribute>
				<gmd:citation>
					<gmd:CI_Citation>
						<gmd:title>
							<xsl:call-template name="writeCharacterString">
								<xsl:with-param name="stringToWrite" select="$title"/>
							</xsl:call-template>
						</gmd:title>
						<xsl:choose>
							<xsl:when test="$dateCnt">
								<xsl:if test="count($creatorDate)">
									<xsl:call-template name="writeDate">
										<xsl:with-param name="testValue" select="count($creatorDate)"/>
										<xsl:with-param name="dateToWrite" select="substring($creatorDate,0,11)"/>
										<xsl:with-param name="dateType" select="'creation'"/>
									</xsl:call-template>
								</xsl:if>
								<xsl:if test="count($issuedDate)">
									<xsl:call-template name="writeDate">
										<xsl:with-param name="testValue" select="count($issuedDate)"/>
										<xsl:with-param name="dateToWrite" select="$issuedDate"/>
										<xsl:with-param name="dateType" select="'issued'"/>
									</xsl:call-template>
								</xsl:if>
								<xsl:if test="count($modifiedDate)">
									<xsl:call-template name="writeDate">
										<xsl:with-param name="testValue" select="count($modifiedDate)"/>
										<xsl:with-param name="dateToWrite" select="substring($modifiedDate,1,10)"/>
										<xsl:with-param name="dateType" select="'revision'"/>
									</xsl:call-template>
								</xsl:if>
							</xsl:when>
							<xsl:otherwise>
								<gmd:date>
									<xsl:attribute name="gco:nilReason"><xsl:value-of select="'missing'"/></xsl:attribute>
								</gmd:date>
							</xsl:otherwise>
						</xsl:choose>
						<xsl:if test="$creatorTotal">
							<xsl:call-template name="writeResponsibleParty">
								<xsl:with-param name="tagName" select="'gmd:citedResponsibleParty'"/>
								<xsl:with-param name="testValue" select="$creatorTotal"/>
								<xsl:with-param name="individualName" select="$creatorName[1]"/>
								<xsl:with-param name="organisationName" select="$institution"/>
								<xsl:with-param name="email" select="$creatorEmail[1]"/>
								<xsl:with-param name="url" select="$creatorURL[1]"/>
								<xsl:with-param name="roleCode" select="'originator'"/>
							</xsl:call-template>
						</xsl:if>
						<xsl:if test="$contributorTotal">
							<xsl:call-template name="writeResponsibleParty">
								<xsl:with-param name="tagName" select="'gmd:citedResponsibleParty'"/>
								<xsl:with-param name="testValue" select="$contributorTotal"/>
								<xsl:with-param name="individualName" select="$contributorName[1]"/>
								<xsl:with-param name="organisationName"/>
								<xsl:with-param name="email"/>
								<xsl:with-param name="url"/>
								<xsl:with-param name="roleCode" select="netcdf/attribute[@name='contributor_role']/@value"/>
							</xsl:call-template>
						</xsl:if>
					</gmd:CI_Citation>
				</gmd:citation>
				<gmd:abstract>
					<xsl:choose>
						<xsl:when test="count(netcdf/attribute[@name='summary']) > 0">
							<xsl:call-template name="writeCharacterString">
								<xsl:with-param name="stringToWrite" select="netcdf/attribute[@name='summary']/@value"/>
							</xsl:call-template>
						</xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="writeCharacterString">
								<xsl:with-param name="stringToWrite" select="netcdf/group[@name='THREDDSMetadata']/group[@name='documentation']/group[@name='document']/attribute[@type='summary']/@value"/>
							</xsl:call-template>
						</xsl:otherwise>
					</xsl:choose>
				</gmd:abstract>
				<srv:serviceType>					<gco:LocalName>
						<xsl:value-of select="$serviceTypeName"/>
					</gco:LocalName>
				</srv:serviceType>

				<srv:couplingType>
					<srv:SV_CouplingType codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml" codeListValue="tight">tight</srv:SV_CouplingType>
				</srv:couplingType>
				<srv:containsOperations>
					<srv:SV_OperationMetadata>
						<srv:operationName>
							<gco:CharacterString>
								<xsl:value-of select="$serviceOperationName"/>
							</gco:CharacterString>
						</srv:operationName>
						<srv:DCP gco:nilReason="unknown"/>
						<srv:connectPoint>
							<gmd:CI_OnlineResource>
								<gmd:linkage>
									<gmd:URL>
										<xsl:value-of select="$operationURL"/>
									</gmd:URL>
								</gmd:linkage>
								<gmd:name>
									<gco:CharacterString>
										<xsl:value-of select="$serviceID"/>
									</gco:CharacterString>
								</gmd:name>
								<gmd:description>
									<gco:CharacterString>
										<xsl:value-of select="$serviceTypeName"/>
									</gco:CharacterString>
								</gmd:description>
								<gmd:function>
									<gmd:CI_OnLineFunctionCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode" codeListValue="download">download</gmd:CI_OnLineFunctionCode>
								</gmd:function>
							</gmd:CI_OnlineResource>
						</srv:connectPoint>
					</srv:SV_OperationMetadata>
				</srv:containsOperations>
				<srv:operatesOn xlink:href="#DataIdentification"/>
			</xsl:element>
		</gmd:identificationInfo>
	</xsl:template>
</xsl:stylesheet>
