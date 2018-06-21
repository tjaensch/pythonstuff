<?xml version='1.0' encoding='UTF-8'?>

<xsl:stylesheet
  xmlns:xsl='http://www.w3.org/1999/XSL/Transform'
  xmlns:gco="http://www.isotc211.org/2005/gco"
  xmlns:gmd='http://www.isotc211.org/2005/gmd'
  version='1.0'
  >

  <xsl:output method='xml' media-type='text/xml' indent='yes' encoding='UTF-8' />

  <!-- string parameter passed into stylesheet names collection metadata file. -->
  <xsl:param name='collFile' />

  <!-- the collection metadata record. -->
  <xsl:variable name='coll' select='document($collFile)' />

  <!-- all valid gmd:MD_Dimensions in the collection metadata record -->
  <xsl:variable name='collDimensions' select='$coll//gmd:axisDimensionProperties/gmd:MD_Dimension[gmd:dimensionName/gmd:MD_DimensionNameTypeCode/@codeList = "http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_DimensionNameTypeCode"]' />

  <!-- all gmd:descriptiveKeywords in the collection metadata record -->
  <xsl:variable name="collKeywords"
    select='$coll//gmd:MD_DataIdentification/gmd:descriptiveKeywords[
    not(contains(gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString, "NCEI ACCESSION NUMBER")) 
    and not(contains(gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString, "NODC DATA TYPES THESAURUS"))
    and not(contains(gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString, "NODC INSTRUMENT TYPES THESAURUS"))
    and not(contains(gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString, "NODC SEA AREA NAMES THESAURUS"))
    and not(contains(gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString, "GCMD Keywords - Instruments"))
    and not(contains(gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString, "GCMD Keywords - Locations"))
    and not(contains(gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString, "NODC PROJECT NAMES THESAURUS"))
    and not(contains(gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString, "NODC ENVIRONMENTAL BUOY THESAURUS"))
    ]'/>

  <!-- start at the top of the granule. -->
  <xsl:template match='/'>
    <xsl:apply-templates />
  </xsl:template>

  <!-- fix bad gmd:resolution elements. -->
  <xsl:template match='gmd:resolution[@gco:nilReason = "missing"]'>
    <!-- look up dimension name in gmd:dimensionName. -->
    <xsl:variable name='dimensionName' select='../gmd:dimensionName/gmd:MD_DimensionNameTypeCode[@codeList = "http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_DimensionNameTypeCode"]/text()' />

    <!-- see if there's a matching dimension in the collection. -->
    <xsl:choose>
      <xsl:when test='$collDimensions[gmd:dimensionName/gmd:MD_DimensionNameTypeCode/text() = $dimensionName]' >
	<!-- found a dimension with the right name in collection; copy it out of the collection. -->
	<xsl:apply-templates select='$collDimensions[gmd:dimensionName/gmd:MD_DimensionNameTypeCode/text() = $dimensionName]/gmd:resolution' mode='collection' />
      </xsl:when>
      <xsl:otherwise>
	<!-- no matching dimension; just copy the gmd:resolution we already have. -->
	<xsl:copy>
	  <xsl:apply-templates select='@*|node()' />
	</xsl:copy>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match='gmd:descriptiveKeywords[position() = last()]'>  
    <!-- copy all of these keywords. -->
	<xsl:copy>
    <xsl:apply-templates />
    </xsl:copy>
	<!--another alternate fix-->
    <!--xsl:apply-templates select='.' mode='collection' /-->
    <!-- copy all the keywords from the collection metadata record. -->
    <xsl:apply-templates select='$collKeywords' mode='collection' />
  </xsl:template>

  <!-- identity transform for everything not matched by something more explicit. (@* matches any attribute node and node() as a pattern "matches any node other than an attribute node)-->
  <xsl:template match='@*|node()' >
    <xsl:copy>
      <xsl:apply-templates select='@*|node()' />
    </xsl:copy>
  </xsl:template>

  <!-- identity transform for collection metadata, used so that other templates aren't applied when copying from the collection (note "mode" attribute). -->
  <xsl:template match='@*|node()' mode='collection' >
    <xsl:copy>
      <xsl:apply-templates select='@*|node()' mode='collection' />
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
