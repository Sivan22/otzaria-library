/* This program is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License version 2
* as published by the Free Software Foundation.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
*
* Author: Moshe Wagner. <moshe.wagner@gmail.com>
*/

//TODO: Take over the world :-)

#include "htmlgen.h"
#include <QDebug>
#include <QTime>
#include "booklist.h"
#include "book.h"
#include <QApplication>
#include <QUrl>

#define QT_USE_FAST_CONCATENATION
#define QT_USE_FAST_OPERATOR_PLUS

//Symbols representing level marks in the text. '!' is the lowest (1), and '^' is the highest (5)
const QString LevelSigns = "!~@^#";

//Font sizes each level's label (in the text itself) should get
const int LevelFontSizeAdd[] = {2,12,18,20,24};

weavedSourceData initWsdFrom (const weavedSource& src)
{
    weavedSourceData ret;
    ret.Title = src.Title;
    ret.FilePath = src.FilePath;
    ret.Zoom = src.Zoom;
    ret.id = src.id;
    ret.show = src.show;
    return ret;
}

//Returns a QString that will be the header of the output HTML file
QString html_head(QString title, QFont font)
{
    QString fontFamily = font.family();
    int basesize = font.pointSize();

    QString t;
    t = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" ";
    t += "\"http://www.w3.org/TR/html4/loose.dtd\">\n";
    t += "<html dir=\"RTL\">\n<head>\n";

    t += "<meta http-equiv=Content-Type content=\"text/html; charset=UTF-8\">";

    t += "\n<title>";
    t += title;
    t += "</title>\n";


    //Add CSS settings to the html file:
    t += CSS(fontFamily, basesize);

#ifndef android
    //Add scripts to the HTML
    t += Script();
#endif

    t +="\n</head>\n";

    return t;
}

// userCss cache
QString userCss = NULL;

QString CSS(QString fontFamily, int basesize)
{
    QString userCssFile = BOOKPATH + "../css/user.css";
    if(NULL == userCss)
        userCss = readfile(userCssFile, "UTF-8");

    QString css = "<style type=\"text/css\">\n"
            "   body { dir=\"RTL\"; text-align:justify; font-family:'" + fontFamily + "'; font-size:" + QString::number(basesize) + "px; }\n"
            //"   A { text-decoration: none; }\n"
            //"   A:hover { color: red; }\n"
//            "   div { line-height: 1.5; }\n"

            "   .L4 { font-family: '" + fontFamily + "'; font-size:" + QString::number(basesize + LevelFontSizeAdd[4]) + "px; font-weight:bold; color:indigo; }\n"
            "   .L3 { font-family: '" + fontFamily + "'; font-size:" + QString::number(basesize + LevelFontSizeAdd[3]) + "px; font-weight:bold; color:indigo; }\n"
            "   .L2 { font-family: '" + fontFamily + "'; font-size:" + QString::number(basesize + LevelFontSizeAdd[2]) + "px; font-weight:bold; color:indigo; }\n"
            "   .L1 { font-family: '" + fontFamily + "'; font-size:" + QString::number(basesize + LevelFontSizeAdd[1]) + "px; font-weight:bold; color:indigo; }\n"
            "   .L0 { font-family: '" + fontFamily + "'; font-size:" + QString::number(basesize + LevelFontSizeAdd[0]) + "px; font-weight:bold; color:indigo; }\n"


            "   .Aliyah { text-align: center; font-family:'" + fontFamily + "'; font-size:" + QString::number(basesize - 4) + "px; font-weight:bold; color:indigo; }\n"
            "   .S0 { font-size:" + QString::number(basesize - 5) + "px;  font-weight:bold;}\n"
            "   .copyright { font-size:" + QString::number((int)(basesize*0.6)) + "px; color:blue;}\n"

            "   .VerySmall { font-size:" + QString::number((int)(basesize*0.7)) + "px;}\n"

            // options from gmara nocha
            "   .ref {font-size:" + QString::number((int)(basesize*0.8)) + "px;}\n"
            "   .pasuk {font-family: \"SBL Hebrew\"; }\n"
            "   .editor {color:#008A00;}\n"
            "   .pirush {color:#2828AC;}\n"
            "   .pirush, .editor{font-size:" + QString::number((int)(basesize*0.9)) + "px;}\n"
            "   .small {font-size:" + QString::number((int)(basesize*0.7)) + "px;}\n"
//add more options...   "   . {;}\n"



            /*
            "   .L4 { font-family: '" + fontFamily + "'; font-size:xx-large; font-weight:bold;}\n"
            "   .L3 { font-family: '" + fontFamily + "'; font-size:xx-large;}\n"
            "   .L2 { font-family: '" + fontFamily + "'; font-size:x-large;  font-weight:bold; }\n"
            "   .L1 { font-family: '" + fontFamily + "'; font-size:x-large; }\n"
            "   .L0 { font-family: '" + fontFamily + "'; font-size:medium; }\n"
            */


            //"   div.Content A { font-family: '" + fontFamily + "'; color:indigo; }\n"
            //"   div.Content A:hover { color:red; }\n"
            "   div.Index A { font-family: '" + fontFamily + "'; color:indigo; }\n"
           // "   div.Index A:hover { color:red; }\n"
            
            

            //adding user defined styles here:
            "" + userCss + "\n"

            "</style>\n";

    return css;
}

//Generate the title part of the Html file
QString html_book_title(QString name, QString copyright, QString low_comments)
{
    QString t="";
    t += "<center><span>";
    if(copyright!="")
    {
        t += "<h3 class=copyright>";
        t +=  QT_TR_NOOP("All right reserved ");
        t +=  "&#169; ";
        t += copyright + "</h3><P>\n";
    }

    t += "<h2>" + name + "<BR></h2>";

    if(low_comments!="")
    {
        t += "<P><h1>";
        t += low_comments + "</h1><P>\n";
    }
    t += "</span></center><P><HR>";
    return t;
}

//Returns html code of a "<a name" tag, for the given name
inline QString namepoint (QString name)
{     return "<a name=\"" + name + "\">&nbsp;</a>\n";          }


//Returns an html link by the given link_to and display text
inline QString link (QString linkto, QString text, int id)
{
    if (linkto.indexOf("$") != -1)
    {
        return "<a id=id_" + stringify(id) + " href=\"" + linkto + "\" style=\"text-decoration:none; color:indigo\" onclick='paintMe(this)' >" + text + "</a> ";
    }
    else if (linkto.indexOf("#") != -1)
    {
        return  "<a href=\"" + linkto + "\" style=\"text-decoration:none\" onclick='paintWhoILinkTo(this)'>" + text + "</a> &nbsp;";
    }
    else
    {
        return  "<a href=\"" + linkto + "\" style=\"text-decoration:none\">" + text + "</a> &nbsp;";
    }
}

//Returns an html link by the given link_to and display text
inline QString genLink(QString linkto, QString text, int id = 0, QString name ="")
{
    if (linkto.indexOf("$") != -1)
    {
        return "<a name=\"" + name + "\" id=id_" + stringify(id) + " href=\"" + linkto + "\" style=\"text-decoration:none; color:indigo\" onclick='paintMe(this)' >" + text + "</a> ";
    }
    else if (linkto.indexOf("#") != -1)
    {
        return  "<a name=\"" + name + "\" href=\"" + linkto + "\" style=\"text-decoration:none\" onclick='paintWhoILinkTo(this)'>" + text + "</a> &nbsp;";
    }
    else
    {
        return  "<a name=\"" + name + "\" href=\"" + linkto + "\" style=\"text-decoration:none\">" + text + "</a> &nbsp;";
    }

}


QString index_to_index(QList <IndexItem> indexitemlist,int level)
{
    QString str="";


    int indexcount = 0;

    str += "<center> &nbsp; <span class=\"VerySmall\">";
    for(unsigned int i=0; i<indexitemlist.size(); i++)
    {
        if(indexitemlist[i].level == level)
        {
            str += reddot();
            str += "&nbsp;" + link("#Index" + stringify(indexcount), indexitemlist[i].displayText);
            str += "&nbsp;";
            //str += "&nbsp;<a href=\"#Index";
            //str += stringify(indexcount);
            //str += "\">";
            //str += indexitemlist[i].displayText + "</a>&nbsp;&nbsp;&nbsp;";
            indexcount++;
        }
    }
    str += "</span>";

    str += "</center>";
    if (indexcount != 0) str += "<HR><BR>";

    return str;
}


QString Script()
{
#ifdef MOBILE
    return "";

#else
    QString str = "<script type=\"text/javascript\">\n";

    //Script showing active part and putting it's link in the status bar
    str += "currentlyPainted=null;\n";
    str += "var currentlyPaintedColor;\n";

    str +="function paintMe(obj) {\n"
          "     if(currentlyPainted)\n"
          "     {\n"
          "            currentlyPainted.style.color = currentlyPaintedColor;\n"
          "     }\n"
          "     currentlyPainted=obj;\n"
          "     currentlyPaintedColor = currentlyPainted.style.color;\n"
          "     obj.focus();\n"
          "     obj.blur();\n"
          "     obj.style.color='red';\n"
          "     window.status = obj.getAttributeNode(\"href\").value\n"
          "}\n";


    str += "function ScrollToElement(theElement) {\n"
           "    var selectedPosX = 0;\n"
           "    var selectedPosY = 0;\n"
           "\n"
           "    while(theElement != null) {\n"
           "        selectedPosX += theElement.offsetLeft;\n"
           "        selectedPosY += theElement.offsetTop;\n"
           "        theElement = theElement.offsetParent;\n"
           "    }\n"
           "    if (selectedPosY < window.pageYOffset || selectedPosY > ((window.innerHeight + window.pageYOffset) * 0.992 ))\n"
           "    window.scrollTo(selectedPosX , selectedPosY);\n"
           "}\n";

    str += "function ReturnValue(varname){\n"
           "    return varname;\n"
           "}\n";

    str +="function ClosestElementToView(){\n"
          "    var closest = null;\n"
          "    var closestoffset = -1 * window.innerHeight;\n"
          "    var i = 0;\n"
          "    var obj = document.getElementById(\"id_\" + i);\n"
          "    while(obj) {\n"
          "       var offset = obj.offsetTop - window.pageYOffset;\n"
          "       if (offset > closestoffset && offset < 10) {\n"
          "           closestoffset = offset;\n"
          "           closest = obj;\n"
          "       }\n"
          "         i++;\n"
          "         var id = \"id_\" + i;\n"
          "         var obj = document.getElementById(id);\n"
          "    }\n"
          "    return closest;\n"
          "}\n";

    str +="function paintById(id) {\n"
          "    var obj = document.getElementById(id);\n"
          "    if (obj) {paintMe(obj); } \n"
          "}\n";

    str += "function findByLink(link) {\n"
           "    var a = document.getElementsByTagName(\"A\");\n"
           "    for(var i=0;i<a.length;i++)\n"
           "    {\n"
           "        if (a[i].href.indexOf(link) != -1)\n"
           "        {\n"
           "            return a[i];\n"
           "        }\n"
           "    }\n"
           "    return null;\n"
           "}\n";

    str += "function paintByHref(href) {\n"
           "    var obj = findByLink(href);\n"
           "    paintMe(obj);\n"
           "}\n";

    str += "function findByAName(link) {\n"
           "    var a = document.getElementsByTagName(\"A\");\n"
           "    for(var i=0;i<a.length;i++)\n"
           "    {\n"
           "        if (a[i].name.indexOf(link) != -1)\n"
           "        {\n"
           "            return a[i];\n"
           "        }\n"
           "    }\n"
           "    return null;\n"
           "}\n";

    str += "function paintByName(name) {\n"
           "    var obj = findByAName(name);\n"
           "    paintMe(obj);\n"
           "}\n";

    str += "function paintWhoILinkTo(obj) {\n"
           "     var p = obj.href.indexOf(\"#\");\n"
           "     paintByHref(\"$\" + obj.href.substr(p+1));\n"
           "}\n";

    str += "function paintNext() {\n"
           "    var i = 0;\n"
           "\n"
           "    if(currentlyPainted)\n"
           "    {\n"
           "        i = parseInt(currentlyPainted.id.substring(3)) + 1;\n"
           "    }\n"
           "    paintById(\"id_\" + i);\n"
           "}\n";

    str += "function paintPrevious() {\n"
           "    var i = 0;\n"
           "    if(currentlyPainted)\n"
           "    {\n"
           "        var num = parseInt(currentlyPainted.id.substring(3)) - 1;\n"
           "        if ( num >= 0 )\n"
           "        {\n"
           "            i = num;\n"
           "        }\n"
           "    }\n"
           "    paintById(\"id_\" + i);\n"
           "}\n";

/*
    str += "document.onkeyup = KeyCheck;       ";
    str += "function KeyCheck()";
    str += "{";
    str += "   var KeyID = event.keyCode;";
    str += "   switch(KeyID)";
    str += "   {";
    str += "      case 37:";
    str += "        paintNext();";
    str += "      break;";
    str += "      case 38:";
    str += "        paintPrevious();";
    str += "      break;";
    str += "      case 39:";
    str += "        paintPrevious();";
    str += "      break;";
    str += "      case 40:";
    str += "        paintNext();";
    str += "      break;";
    str += "   }";
    str += "}";
*/
    str += "function addComment (name, comment) {\n"
           "  if ( comment != '' ){"
           "    var newLink = document.createElement('a');\n"
           "    newLink.href  = '*' + name;\n"
           "    newLink.setAttribute('style', 'text-decoration:none; color:blue; font-size:14px');\n"
           "    var newLinkText = document.createTextNode(' [*] ' + comment);\n"
           "    newLink.appendChild(newLinkText);"
           "  }\n"
           "  var nameElem = document.getElementsByName(name)[0];\n"
           "  if (nameElem != null){\n"
           "    var commentExists = findByLink('*' + name);\n"
           "    if ( commentExists != null ) nameElem.removeChild(commentExists);\n"
           "    if ( comment != '' ) nameElem.appendChild(newLink);\n"
           "  }\n"
           "}\n";

    str += "</script>\n";

    return str;
#endif //not mobile
}

//External links:

//Returns the Html code for the given external link
QString ExternalLink (QString linkcode)
{
    bool ToraOr;
    bool ShouldBePrintedOnNewLine;
    //UniqueId of target link
    int  BookUniqueId = 0;
    //Label within the target book
    QString BookInternalLabel = "";
    //Link's display name
    QString DisplayedText = "";
    //Link's display style
    int  DisplayStyle = 0;  // BITS:  0-bold, 1-underline, 2-italic, 3-small, 4-big, 5-red, 6-green, 7-blue

    //Validate line
    if (linkcode.startsWith("<!--ex") == false)
        return "";

    //Check type
    if (linkcode[6] == 'a')
    {
        ToraOr = false;
        ShouldBePrintedOnNewLine = false;
    }
    else if (linkcode[6] == 'b')
    {
        ToraOr = false;
        ShouldBePrintedOnNewLine = true;
    }
    else if (linkcode[6] == 'c')
    {
        ToraOr = true;
        ShouldBePrintedOnNewLine = false;
    }
    else
        return "";

    //Find location of "-->"
    size_t ptr = linkcode.indexOf("-->");

    //Get displayed text
    DisplayedText = linkcode.mid(ptr+3, linkcode.length()-1);

    //Get data : skip the first 7 chars - cut of the lenth of the displayed text and the "-->"
    QString Data = linkcode.mid(7, ptr-4);  //linkcode.mid(0, ptr+3).mid(7);

    //Decrypt link, and convert the data to unicode
    QByteArray qba = Decrypt(string(Data.toUtf8()), true).c_str();
    QTextCodec * codec = QTextCodec::codecForName("ISO-88598");
    Data = codec->toUnicode(qba);

    if (Data == "")
        return "";

    //Split to parts
    QStringList split_up = Data.split("|");

    //Get display style
    if (!ToNum( split_up[0], &DisplayStyle))
        return "";

    if(split_up[1]!="")
    {
        //If part starts with "bm:"
        if(split_up[1].startsWith("bm:"))
        {
            //Find #
            ptr = split_up[1].indexOf("#");
            //Get BookUniqueId
            if(!ToNum(split_up[1].mid(3, ptr-4), &BookUniqueId))
                return "";
            //Get BookInternalLabel
            BookInternalLabel = split_up[1].mid(ptr+1);
        }
    }

    QString Html="";

    // DisplayStyle BITS:  0-bold, 1-underline, 2-italic, 3-small, 4-big, 5-red, 6-green, 7-blue
    int DS = DisplayStyle;

    //I'm ignoring the coloers at the moment
    if ( DS>>0 & 0x1 ) Html += "<B>";
    //if ( DS>>1 & 0x1 ) Html += "<U>";
    if ( DS>>2 & 0x1 ) Html += "<I>";
    //if ( DS>>3 & 0x1 ) Html += "<small>";
    if ( DS>>4 & 0x1 ) Html += "<big>";

    //if (ShouldBePrintedOnNewLine)
    //    Html += "<BR>\n";

    // Eliminate spaces
    QString  linkto = BookInternalLabel;

    //Escape the hebrew chars
    linkto = escapeToBase32(linkto);

    if (BookUniqueId != 0)
    {
        Html += "<a href=\"!" + stringify(BookUniqueId);
        Html += ":" +  linkto + "\">";
        Html += DisplayedText + "</a>\n";
    }
    else
    {
        Html += DisplayedText;
    }

    //I'm ignoring the coloers at the moment
    //revert order to respect html tags nested
    if ( DS>>4 & 0x1 ) Html += "</big>";
    //if ( DS>>3 & 0x1 ) Html += "</small>";
    if ( DS>>2 & 0x1 ) Html += "</I>";
    //if ( DS>>1 & 0x1 ) Html += "</U>";
    if ( DS>>0 & 0x1 ) Html += "</B>";

    return Html;
}

//I have no idea how this works, it just does.
// Many thanks to the developer of the original program
string Decrypt (string text, bool decrypt)
{
    string ret;

    ret = text;
    ret += text;  // allocate buffer
    unsigned char *s = (unsigned char *)(text.c_str());
    unsigned char *d = (unsigned char *)(ret.c_str());

    //Encrypt
    if (!decrypt)
    {
        while (*s)
        {
            *(d++) = 'A' + ((*s) & 15);
            *(d++) = 'A' + (((*(s++)) >> 4) & 15);
        }
        return ret;
    }
    //Decrypt
    else
    {
        while (*s && s[1])
        {
            (*d)  =  (*(s++) - 'A');
            (*(d++)) |=  (*(s++) -  'A') << 4;
        }
        return ret;
    }
    //Failure
    return "";
}



/*
  Chapter loading :

  TODO:
  - Release loaded books
  - Test
  - Bookmarks
  - Clean code
  - Comments, etc'

  */


//This function reads the book's text, split up to 'Lowest Index Levels',
// into the 'chapterText' list, while the equivilant Iters are stored in the 'chapterIter' list.
void Book::readBook(int LowsetIndexLevel)
{
    //Don't load book twice
    if (chapterIter.size() > 0) return;

    //Read text into vector
    QList <QString> text;

    //Read the source file associated to this book:
    QString zipfile = absPath(mPath);
    if( !ReadFileFromZip(zipfile, "BookText", text, "UTF-8", true, isEncrypted) )
    {
        print( "ERROR: Unable to open zipfile: " + zipfile + " !");
        return ;
    }

    //See file isn't empty...
    if ( text.size() < 2 )
    {
        print( "ERROR: Invalid file: " + zipfile + " !");
        return ;
    }


    //Find real LIL
    //Levels possible here are 1,2,3,4,5
    bool haslevel[5]={false};

    for(int i=0; i<text.size(); i++)
    {
        int level = LevelSigns.indexOf(text[i][0]);
        if ( level > 0 && level < 6)
        {
            haslevel[level - 1] = true;
        }
    }

    //Get LevelMIN to one above the lowest existing level:

    unsigned int levelMIN=0, higherLevel=0;
    //Find lowest level
    for (levelMIN=0; levelMIN < 4 && haslevel[levelMIN] == false; levelMIN++) {};

    /*
    //Find the next one above it:
    for (higherLevel = levelMIN + 1 ; higherLevel < 4 && haslevel[higherLevel] == false; higherLevel++) {};

        higherLevel += 1;
        */
    // (The found numbers are 1 under the real level, because they started from 0 and the levels start from 1)
    levelMIN ++;

    if (levelMIN > 1 && LowsetIndexLevel == 1)
    {
        LIL = levelMIN;
        LowsetIndexLevel = LIL;
    }


    //Validate LIL
    if (LowsetIndexLevel < 0 || LowsetIndexLevel >= LevelSigns.size()) return;


    buildIndex(text);

    BookIter itr;

    QStringList t;
    //Go over lines, see where levelsigns are
        //Build iter for level sign
    for(int i=0; i<text.size(); i++)
    {
        int level;

        //If it's one of the level signs
        if ( (level = LevelSigns.indexOf(text[i][0])) != -1 )
        {
            //Advance the book itr to the new position
            itr.SetLevelFromLine(text[i]);

            //Advance chapter text & iter


            //UGLY HACK! Hope this works well...
            if (level > LowsetIndexLevel)
            {
                //If this level, that is higher than LIL, comes right before it,
                // treat it as if was the LIL sign (and ignore the LIL after it, of course)
                for (int j = i + 1; (LevelSigns.indexOf(text[j][0]) > 0 || text[j].simplified() == "")  && j < text.size(); j++ )
                {
                    if (LevelSigns.indexOf(text[j][0]) == LowsetIndexLevel)
                    {
                        itr.SetLevelFromLine(text[j]);

                        chapterIter.append(itr);
                        chapterText.append(t);

                        t.clear();
                        //Add the level signs above the LIL
                        for (int k=i; k<=j; k++)
                        {
                            t.append(text[k]);
                        }

                        i = j + 1;
                    }
                }
            }
            else if (level == LowsetIndexLevel)
            {
                chapterIter.append(itr);
                chapterText.append(t);
                t.clear();
            }

            t.append(text[i]);

        }
        else
        {
            if (this->PutNewLinesAsIs) text[i] += "<BR>";
            t.append(text[i]);
        }
    }

    if (!t.isEmpty())
    {
        chapterText.append(t);
    }

    //The first chapterText is all what came before the first relevant itr, so we don't need it
    if (chapterText.size() > 1) chapterText.removeFirst();

}

//Return html code of dots:
QString bluedot()
{ return "<span style=\"color:blue\"><B>&bull;</B></span>"; }

QString reddot()
{ return "<span style=\"color:red\"><B>&bull;</B></span>";  }


//Returns the index (תוכן) of the book
void Book::buildIndex(QList <QString> text)
{
    indexitemlist.empty();

    BookIter itr;

    for(int i=0; i<text.size(); i++)
    {
        int level = LevelSigns.indexOf(text[i][0]);
        if ( level > 0)
        {
            itr.SetLevelFromLine(text[i]);

            IndexItem indexitem;

            indexitem.level = level + 1;

            if (level == LIL)
            {
                indexitem.linkPoint =  "@" + itr.toEncodedString();
            }

            //Display of link levels in the Html itself, and in the index
            QString dispname;

            //If the book is a gmara, give the pages (that are level 1) thier special names:
            if ( (mPath.contains("תלמוד") || mPath.contains("שס")) && ( level == 1) )
            {
                dispname = itr.gmaraDisplay();
            }
            else
            {
                vector <QString> tmp;
                //If only part of the link name should be in the index - cut it.
                if(mRemoveSuffix[level] != "")
                {
                    splittotwo ( text[i].mid(2), tmp, mRemoveSuffix[level]);
                    if(tmp[1] != "")
                        dispname = tmp[1];
                    else
                        dispname = tmp[0];

                    tmp.clear();
                }
                else
                {
                    dispname = text[i].mid(2);
                }
            }

            indexitem.displayText = dispname;

            //Add the new indexitem to the indexitems list
            indexitemlist.push_back(indexitem);
        }
    }



}

QString html_link_table(QList <IndexItem> indexitemlist, int short_index_level, bool dot, bool hasRUS)
{

    //TODO: Make those in tables look better (streach to both sides?)

    //NOTE: This is a bit tricksy (see LOTR if you don't know that word),
    //      this should be tested with more books, and documented a lot more

    QString link_table="";
    bool opentable = false;
    int iln = 0;

    //Levels possible here are 2,3,4,5
    bool haslevel[4]={false};


    for (unsigned int i=0; i<indexitemlist.size(); i++)
    {
        if (indexitemlist[i].level == 2)
            haslevel[0] = true;
        if (indexitemlist[i].level == 3)
            haslevel[1] = true;
        if (indexitemlist[i].level == 4)
            haslevel[2] = true;
        if (indexitemlist[i].level == 5)
            haslevel[3] = true;
    }


    //Get LevelMIN to one above the lowest existing level:

    unsigned int levelMIN=0, higherLevel=0;
    //Find lowest level
    for (levelMIN=0; levelMIN < 4 && haslevel[levelMIN] == false; levelMIN++) {};

    //Find the next one above it:
    for (higherLevel = levelMIN + 1 ; higherLevel < 4 && haslevel[higherLevel] == false; higherLevel++) {};

    // (The found numbers are 2 under the real levels, because they started from 0 and the levels start from 2)
    levelMIN += 2;
    higherLevel += 2;


    //If only one link level is present (and thus higherLevel became 6)
    if ( higherLevel == 6)
    {
        link_table += "<span class=\"L0\">&nbsp;";
        for (unsigned int j=0; j<indexitemlist.size(); j++)
        {
            link_table += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
            link_table += bluedot() + "&nbsp;";

            link_table += genLink(indexitemlist[j].linkPoint, indexitemlist[j].displayText);

            if (!hasRUS) link_table +="<BR>\n";
        }
        link_table += "</span>";
    }

    //If more than one level,
    // the lowest is in a table under the one closest above it,
    // and the higher one(s) get a <P> before them.
    else
    {
        for (unsigned int j=0; j<indexitemlist.size(); j++)
        {
            if (opentable && indexitemlist[j].level >= higherLevel)
            {
                link_table += "<P></td></tr></tbody></table>";
                opentable = false;
            }

            if(short_index_level == indexitemlist[j].level)
            {
                QString name = "Index"+ stringify(iln);
                link_table += "<a name=\"" + name + "\" " + "href=\"$" + name + "\"></a>\n";
                iln ++;
            }

            //Higher than one above the lowest
            if (indexitemlist[j].level > higherLevel)
            {
                link_table += "<P><span class=\"L1\">&nbsp;";

                link_table += genLink(indexitemlist[j].linkPoint, indexitemlist[j].displayText);
                link_table += "</span>\n";
            }
            else if (indexitemlist[j].level == higherLevel)
            {
                link_table += "<span class=\"L0\">&nbsp;";

                link_table += genLink(indexitemlist[j].linkPoint, indexitemlist[j].displayText);
                link_table +=  "</span>\n";
                link_table += "<table border=\"0\" cellpadding=\"8\" cellspacing=\"2\" width=\"100%\"><tbody><tr><td width=\"24\"><td align=\"right\">";
                opentable = true;
            }
            else
            {
                if(dot)
                    link_table += bluedot() + " " + genLink(indexitemlist[j].linkPoint, indexitemlist[j].displayText);
                else
                    link_table += genLink(indexitemlist[j].linkPoint, indexitemlist[j].displayText);
                link_table +="&nbsp;\n";
            }

        }
    }
    if (opentable)
        link_table += "</td></tr></tbody></table>";

    if (link_table != "") link_table += "<HR>";

    return link_table;
}



QUrl Book::renderBookIndex()
{
    static int ind = 0;

    QString html = "";
    html += html_head(mNormallDisplayName, getFont());

    html += "<body";

    if(nightMode)
        html += " class=\"nightMode\"";

    html += ">";

    html += html_book_title(mNormallDisplayName, mCopyrightInfo, "");

    html += "<div class=\"Index\">";

    //IZAR: moved here to create quicker access to index
    html += namepoint("Top");

    //html += "<center><i>" + genLink("@5 ", "הצג את כל הספר") + "</i></center><br><br>\n";

    //IZAR
    // try to geuss the short index level
    if (mShortIndexLevel < 1 && indexitemlist.size() > 0)
    {

        //mShortIndexLevel = indexitemlist[0].level;

        //get the higest and lowest level in use
        int highetLVL = 0 , lowestLVL = 100;
        foreach(IndexItem item, indexitemlist)
        {
            if (item.level > highetLVL) highetLVL = item.level;
            if (item.level < lowestLVL) lowestLVL = item.level;
        }
        if (highetLVL > lowestLVL) mShortIndexLevel = highetLVL;

        //qDebug()<< "short index level geuss: " << mShortIndexLevel ;
    }


    //Book with no chapters:
    if (indexitemlist.size() == 0)
    {
        //Read text into vector
        QList <QString> text;

        //Read the source file associated to this book:
        QString zipfile = absPath(mPath);
        ReadFileFromZip(zipfile, "BookText", text, "UTF-8", true, isEncrypted);

        for (int i=0; i<text.size(); i++) if (text[i][0] != '$') html += text[i] + "<BR>\n";
    }

    //TODO: @@@
    html +=  index_to_index(indexitemlist, mShortIndexLevel);
    html +=  html_link_table(indexitemlist, mShortIndexLevel, true, true);


    html += "</div></body></html>";

    //qDebug() << "/n/n--------------------/nindex html:\n" << html;
    //return html;

    QString path = TMPPATH + "Index" + QString::number(ind++) + ".html";
    writetofile(path, html, "UTF-8", true);

    return QUrl::fromLocalFile(path);
}

//Returns the Html to display of the chapter given by the iter.

QUrl Book::renderChapterHtml(BookIter iter, BookList * booklist, bool shownikud, bool showteamim, QRegExp mark)
{
    static int ind = 0;

    bool FullChapterWeaveMode = false;
    if (LevelSigns.indexOf(WeaveLevel) == LIL) FullChapterWeaveMode = true;

//    qDebug() << FullChapterWeaveMode;

    //ignore invalid iters
    if (iter.isEmpty()) return QUrl();

    QList <weavedSourceData> Sources;
    for (int i=0; i<mWeavedSources.size(); i++)
    {
        if (mWeavedSources[i].show == true)
        {
            weavedSourceData src = initWsdFrom ( mWeavedSources[i] );
            Sources.append(src);
        }
    }

    //Show only this book
    if (mWeavedSources.size() == 0)
    {
        weavedSourceData src;
        src.id = mUniqueId;
        src.show = true;
        src.Prefix = "";
        src.Suffix = "";

        Sources.append(src);
    }

    QStringList colors;
    colors << "#009000" << "#0000FF" << "#A52A2A" << "#4B0082";
    for (int i=1; i<Sources.size(); i++)
    {
        int j = ((i - 1) % colors.size());

        //Title is now before the text, not after
        if (Sources[i].Prefix == "")
        {
            Sources[i].Prefix = "<span style= color:" + colors[j] + ">";
            Sources[i].Prefix += "<i><b> " +  Sources[i].Title + ": </b></i><br>";
        }
        if (Sources[i].Suffix == "") Sources[i].Suffix = "</span>";
        //if (Sources[i].Suffix == "") Sources[i].Suffix = "<small> [" +  Sources[i].Title + "] </small></span>";
    }

    QString html = "";
    html += html_head(mNormallDisplayName, getFont());

    html += "<body";

    if(nightMode)
        html += " class=\"nightMode\"";

    html += ">";

    html += "<div class=\"Content\">";

    //html += namepoint("Top");

    QString last_label = "";

    //Load all sources to the memory:
    for (int i=0; i<Sources.size(); i++)
    {
        Sources[i].text.clear();

        Book *b;
        if (i == 0) b = this;
        else b = booklist->FindBookByPath(Sources[i].FilePath);

        //qDebug() << i << Sources[i].FilePath;

        if (b)
        {
            //TODO: Prevent double reading
            b->readBook(LIL);

            //Try comparing the iter's the right way:
            int n = -1;
            for (int j=0; j < b->chapterIter.size(); j++)
            {
                if (iter.toString(LIL).indexOf(b->chapterIter[j].toString(LIL)) != -1) n = j;
            }

            //If it wasn't found by the orthodox way, it's probably a link...
            if (n == -1)
            {
                //Compare link iters using the humanDisplay system, or it won't work...
                QString ia = iter.humanDisplay();

                for (int j=0; j < b->chapterIter.size() && j < b->chapterText.size(); j++)
                {
                    QString ib = b->chapterIter[j].humanDisplay();

                    if (ia.indexOf(ib) != -1) n = j;
                    if (n == -1)  if (ib.indexOf(ia) != -1) n = j;
                }
            }

            if (n < 0 || n >= b->chapterText.size() || n >= b->chapterIter.size()) Sources[i].text.clear();
            else Sources[i].text = b->chapterText[n];

            /*
            if (LIL > 4 && b->chapterText.size() > 0)
            {
                Sources[i].text = b->chapterText[0];
            }
            */
        }

        Sources[i].str = "";
        Sources[i].line = 0;
    }

    //BEWARE: Super ugly hack; But it's still better than what we had before.
    //Add a fake level sign to the end of the main source, so we know we're done
    Sources[0].text.push_back("! {EOF}");


    //for (int i=0; i<Sources.size(); i++) qDebug() << Sources[i].text;

    //Go over every line in the main source:
    for (int i=0; i<Sources[0].text.size(); i++)
    {
        //Be nice to other people too
        QApplication::processEvents();

        //Use the first line of whats left of the file, and chop it off
        QString line = Sources[0].text[i];

        //Display nikud and teamim depending on the NikudMode
        if ( hasNikud && shownikud == false) line = removeNikud(line);
        if ( hasTeamim && showteamim == false) line = removeTeamim(line);

        //A new level is reached, so add all that came before it to the Html, and get all of the sources' text for this level
        //NOTE: this is a bit funny (think about it). Maybe this should be fixed. But it still works...
        int level;
        if ( (level = LevelSigns.indexOf(line[0])) != -1 )
        {
            //In full chapter mode the other sources are dealt with outside the loop
            if (!FullChapterWeaveMode)
            {
                // Go over all other sources
                for (int j=1; j<Sources.size(); j++)
                {
                    if (Sources[j].line < Sources[j].text.size())
                    {
                        //Update the sources' itr to this line
                        // (It should be a level line that matters, because the loop doesn't stop before that)
                        Sources[j].itr.SetLevelFromLine(Sources[j].text[Sources[j].line]);



                        //If the iters don't match, maybe the source has two iter lines one after another.
                            //This UGLY HACK tries to fix it if thats the case
                        if (Sources[0].itr != Sources[j].itr)
                        {
                            int nextline = Sources[j].line + 1;
                            if (nextline < Sources[j].text.size())
                            {
                                BookIter tmpitr(Sources[j].itr);

                                QString s = Sources[j].text[nextline];

                                //As long as the file didn't end and no level that matters was changed, keep on adding text
                                while ( (nextline < Sources[j].text.size()) && ((s.replace("\n","").simplified() == "" ) || (LevelSigns.indexOf(s[0]) != -1)))
                                {
                                    tmpitr.SetLevelFromLine(s);

                                    if (tmpitr == Sources[0].itr)
                                    {
                                        Sources[j].itr.SetLevelFromLine(s);
                                    }

                                    nextline ++;
                                    s = Sources[j].text[nextline];
                                }
                            }
                        }


                        //If it's the same as the one level just passed in the main source, add this level's text to the Html too.
                        if (Sources[0].itr == Sources[j].itr)
                        {
                            Sources[j].line ++;

                            QString source_line = Sources[j].text[Sources[j].line];

                            //Clone the sources' itr, so we can see if it changed
                            BookIter tmpitr(Sources[j].itr);
                            tmpitr.SetLevelFromLine(source_line);

                            //As long as the file didn't end and no level that matters was changed, keep on adding text
                            while ( (tmpitr == Sources[0].itr) && (Sources[j].line < Sources[j].text.size()))
                            {
                                if (LevelSigns.indexOf(source_line[0]) == -1)
                                {
                                    //TODO: Why not enable links in commentaries?
                                    if (!source_line.startsWith("<!--"))
                                    {
                                        Sources[j].str += source_line + "\n";
                                    }
                                }

                                Sources[j].line ++;

                                if (Sources[j].line < Sources[j].text.size())
                                {
                                    //Update the cloned itr
                                    source_line = Sources[j].text[Sources[j].line];
                                    tmpitr.SetLevelFromLine(source_line);
                                }
                            }
                        }
                    }
                }
            }

            if (last_label != "")
            {
                for (int j=0; j<Sources.size(); j++)
                {
                    if ( Sources[j].str.replace("\n", "") != "" )
                    {
                        html += Sources[j].Prefix;
                        html += Sources[j].str;
                        html += Sources[j].Suffix;
                        if (!this->PutNewLinesAsIs)
                            html += "<BR>\n";
                        if (Sources.size() > 1)
                            html += "<BR>\n";
                    }
                }
            }

            last_label = line;

            //Emtpy strs
            for (int j=0; j<Sources.size(); j++) Sources[j].str.clear();

            /*
            //See if the is a comment for the past position, and if so, insert it now
            vector<QString>::iterator vitr = find(comment_titles.begin(), comment_titles.end(), lastlink);
            int index = distance (comment_titles.begin (), vitr);
            if (index != comment_titles.size())
            {
                QString comment = " [*] " + comment_texts[index].replace("\\|", "|").replace("|", "<BR>");

                //Add the text as a special link so menu's can be opened here (and know where this is)
                htmlbody += "<a href=\"*" + last_label + "\" style=\"text-decoration:none; color:blue; font-size:14px\">";
                htmlbody += comment + "</a>";
            }
            */

            //Deal with the level sign for this book itself:

            //Advance itr:
            Sources[0].itr.SetLevelFromLine(line);

            if (Sources[0].itr.humanDisplay().indexOf("EOF") == -1)
            {
                QString strforlink = Sources[0].itr.toEncodedString(level + 1);

                if (!PutNewLinesAsIs||level>0)
                    html+="<BR>";
                html += "<span class=\"L" + QString::number(level) + "\">";
                html += "<a name=\"" + strforlink + "\">";

                //Add the text as a special link so menu's can be opened here (and know where this is)
                //htmlbody += link("$" + strforlink, dispname, linkid);
                //linkid ++;

                html += Sources[0].text[i].mid(2);
                html += "</a></span>\n";
                if (level != 0 )
                    html += "<BR>";
            }
        }

        //External link ("<!--ex" type)
        else if(line.startsWith("<!--ex"))
        {
            //htmlbody += ExternalLink(line);
            Sources[0].str += ExternalLink(line);
        }
        else
        {
            //Hope this is OK... Not realy tested yet
            //Run all pre-set replaces
            for (int i=0; i<replaceFrom.size(); i++)
            {
                line.replace(replaceFrom[i], replaceTo[i]);
            }

            if (mark.pattern() != "()" && mark.pattern() != "")
                line.replace(mark, "<span style=\"background-color:#FFF532\">\\1</span>");

            Sources[0].str += line + " ";
        }
    }


    //This is important for cases where we need to force whole chapter weaving,
    // becuase otherwise it won't weave properly. i.e., when the sub-chapters of the sources aren't of the same type.
    if (FullChapterWeaveMode)
    {
        for (int i=1; i<Sources.size(); i++)
        {
            QString t = "";
            for (int j=1 /* Skip iter line*/ ; j<Sources[i].text.size(); j++) t += Sources[i].text[j] + "\n";
            t = t.simplified();

            if (!t.isEmpty())
            {
                html += Sources[i].Prefix;
                html += t;
                html += Sources[i].Suffix;
                if (!this->PutNewLinesAsIs)
                    html += "<BR>\n";
                if (Sources.size() > 1)
                    html += "<BR>\n";
            }
        }
    }


    for (int i=0; i<Sources.size(); i++) Sources[i].text.clear();

    html += "</div>";
    html += "</body>\n</html>";

    //return html;

    QString path = TMPPATH + "HTML" + QString::number(ind++) + ".html";
    writetofile(path, html, "UTF-8", true);

    return QUrl::fromLocalFile(path);
}
