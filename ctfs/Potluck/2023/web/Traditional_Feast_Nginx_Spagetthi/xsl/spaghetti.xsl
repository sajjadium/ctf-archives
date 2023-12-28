<xsl:stylesheet version="1.1" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:exsl="http://exslt.org/common" xmlns:str="http://exslt.org/strings" extension-element-prefixes="exsl str">
  <xsl:output method="xml" media-type="text/xml" />
  
  <xsl:template match="/">
    <msg>TFNS</msg>
    <exsl:document href="{str:decode-uri($filename)}" method="xml">
      <xsl:apply-templates />
    </exsl:document>
  </xsl:template>

  <!-- Create new spaghetti -->
  <xsl:template match="/new">
    <spaghetti>
      <counter>0</counter>
      <name>
        <xsl:value-of select="str:decode-uri(str:replace($name, '+', ' '))" />
      </name>
      <image>
        <xsl:value-of select="str:decode-uri(str:replace($image, '+', ' '))" />
      </image>
      <xsl:variable name="decoded_recipe" select="str:decode-uri(str:replace($recipe, '+', ' '))" />
      <xsl:choose>
        <!-- If the recipe contains ingredients -->
        <xsl:when test="contains($decoded_recipe, '&#x0d;&#x0a;&#x0d;&#x0a;')">
          <xsl:call-template name="recipe">
            <xsl:with-param name="ingredients" select="substring-before($decoded_recipe, '&#x0d;&#x0a;&#x0d;&#x0a;')" />
            <xsl:with-param name="instructions" select="substring-after($decoded_recipe, '&#x0d;&#x0a;&#x0d;&#x0a;')" />
          </xsl:call-template>
        </xsl:when>
        <!-- Else -->
        <xsl:otherwise>
          <xsl:call-template name="recipe">
            <xsl:with-param name="ingredients" select="''"  />
            <xsl:with-param name="instructions" select="$decoded_recipe" />
          </xsl:call-template>
        </xsl:otherwise>
      </xsl:choose>
    </spaghetti>
  </xsl:template>

  <!-- Increment visitor counter -->
  <xsl:template match="/spaghetti">
    <spaghetti>
      <counter>
        <xsl:value-of select='./counter + 1' />
      </counter>
      <xsl:copy-of select="./*[not(self::counter)]" />
    </spaghetti>
  </xsl:template>

  <!-- Internal recipe template -->
  <xsl:template name="recipe">
    <xsl:param name="ingredients" />  
    <xsl:param name="instructions" />  

    <!-- Iter over ingredients -->
    <xsl:for-each select="str:tokenize($ingredients,  '&#x0d;&#x0a;')">
      <ingredient>
        <name>
          <xsl:value-of select="substring-before(., ':')" />
        </name>
        <quantity>
          <xsl:value-of select="substring-after(., ':')" />
        </quantity>
      </ingredient>
    </xsl:for-each>

    <!-- Allow HTML in recipe -->
    <recipe>
      <xsl:value-of select="concat('&lt;![CDATA[', $instructions, ']]&gt;')" disable-output-escaping="yes" />
    </recipe>
  </xsl:template>
</xsl:stylesheet>