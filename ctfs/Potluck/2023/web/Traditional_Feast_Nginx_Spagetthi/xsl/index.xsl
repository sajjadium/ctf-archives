<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output
    method="html"
    doctype-public="spaghetti"
    omit-xml-declaration="yes"
    encoding="UTF-8"
    indent="yes"
  />
  <xsl:template match="/">
    <html>
      <head>
        <title><xsl:value-of select="//*[self::title or self::name]" /></title>
        <script src="https://cdn.tailwindcss.com"></script>
      </head>
      <body class="bg-red-900 flex items-center justify-center h-screen">
        <div class="text-center p-6 max-w-xl mx-auto bg-white rounded-xl shadow-lg shadow-black">
          <xsl:apply-templates />
        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="/page">
    <h1 class="text-2xl font-bold mb-2">
      <xsl:value-of select="./title" />
    </h1>
    <p class="text-gray-700 mb-4">
      <xsl:value-of select="./content" />
    </p>
    <xsl:for-each select="./form">
      <form action="{@target}/{$request_id}" class="flex flex-col space-y-4">
        <xsl:for-each select="./input">
          <xsl:choose>
            <xsl:when test="@type = 'text'">
              <input
                type="text"
                name="{@name}"
                required="true"
                placeholder="{@name}"
                class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-300"
              />
            </xsl:when>
            <xsl:when test="@type = 'textarea'">
              <textarea
                name="{@name}"
                placeholder="{@name}"
                class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-300"
              ></textarea>
            </xsl:when>
            <xsl:when test="@type = 'button'">
              <button
                type="submit"
                class="bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded"
              >
                <xsl:value-of select="@label" />
              </button>
            </xsl:when>
            <xsl:when test="@type = 'select'">
              <label class="self-start text-gray-700">
                <xsl:value-of select="@label" />
              </label>
              <select
                name="{@name}"
                value="{@value}"
                class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-300"
              >
                <xsl:for-each select="./option">
                  <option value="{.}">
                    <xsl:value-of select="." />
                  </option>
                </xsl:for-each>
              </select>
            </xsl:when>
          </xsl:choose>
        </xsl:for-each>
      </form>
    </xsl:for-each>
  </xsl:template>
  <xsl:template match="/spaghetti">
    <div class="relative flex flex-col justify-end text-white min-w-[400px] min-h-[400px]">
      <img src="/img/{./image}.jpg" class="absolute" />
      <div class="flex-1" />
      <div class="backdrop-blur-lg bg-black/20 p-4">
        <h1 class="text-2xl font-bold mb-4 uppercase font-thin">
          <xsl:value-of select="./name" />
        </h1>

        <div class="mb-2">
          <div class="font-bold">Ingredients:</div>
          <ul>
            <xsl:for-each select="./ingredient">
              <li class="flex gap-4">
                <span class="text-white font-bold"> <xsl:value-of select="./name" />: </span>
                <span class="text-red-200">
                  <xsl:value-of select="./quantity" />
                </span>
              </li>
            </xsl:for-each>
          </ul>
        </div>
        <div class="mb-2">
          <div class="font-bold">Recipe:</div>
          <pre class="text-red-200 whitespace-pre">
            <xsl:value-of select="./recipe" disable-output-escaping="yes" />
          </pre>
        </div>
        <div class="mb-2">
          <span class="font-bold">Visitors: </span>
          <span class="text-red-200">
            <xsl:value-of select="./counter" />
          </span>
        </div>
      </div>
      <div class="flex-1" />
      <div class="flex gap-2 p-2 backdrop-blur-lg bg-black/20 text-sm z-10">
        Download as:
        <a class="text-yellow-400 hover:underline font-bold" href="/download/{$spaghetti_id}.xml"
          >XML</a
        >
        <a class="text-yellow-400 hover:underline font-bold" href="/download/{$spaghetti_id}.json"
          >JSON</a
        >
      </div>
    </div>
  </xsl:template>
</xsl:stylesheet>
