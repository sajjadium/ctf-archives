<?xml version="1.0" encoding="iso-8859-1" standalone="yes"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                version="1.0">
<xsl:output method='html'/>
<xsl:template match='/'>
<html>
  <body>
  <h1>Stats for Country: %%COUNTRY%%</h1>
    <table border="1">
      <tr>
        <th>Year</th>
        <th>Population</th>
      </tr>
        <xsl:for-each select="Root/data/record">
          <xsl:variable name="country" select="field[@key]" />
          <xsl:variable name="year" select="field[@name='Year']" />

          <xsl:if test="contains($country,'%%COUNTRY%%') and number($year) &gt; number('%%STARTYEAR%%') and number($year) &lt; number('%%ENDYEAR%%')">
            <tr>
              <td><xsl:value-of select="field[@name='Year']/text()"/></td>
              <td><xsl:value-of select="field[@name='Value']/text()"/></td>
            </tr>
          </xsl:if>
        </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>