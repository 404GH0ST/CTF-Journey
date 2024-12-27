<!DOCTYPE html>
<html>
<head>
    <title>LINECTF2024 | jalyboy-baby</title>
    <style>
    .center {
      display: flex;
      align-items: center;
      justify-content: center;
      -webkit-flex-direction: column;
   　　flex-direction: column;
      height: 100vh;
    }
    .light {
        background-color: #f0f0f0;
        color: #333;
    }
    .dark {
        background-color: #333333;
        color: #f0f0f0;
    }
    .button {
        display: inline-block;
        padding: 10px 20px;
        margin: 5px;
        background-color: #007bff;
        color: white;
        text-align: center;
        text-decoration: none;
        border: none;
        border-radius: 5px;
        transition: box-shadow 0.2s, transform 0.2s;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    .button:hover {
        text-decoration: none;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        transform: translateY(1px);
    }
    .button.disabled, .button:disabled {
        background-color: #ccc;
        color: #666;
        cursor: not-allowed;
        box-shadow: none;
        pointer-events: none;
    }
    </style>
</head>
<body class="dark">
    <div class="center">
        <h1>LINECTF2024 | jalyboy-jalygirl</h1>
        <h2>Hi ${sub}!</h2>
        <#if flag?has_content>
            <p>flag is <code>${flag}</code> &#x1f389;</p>
        </#if>
        <div>
            <a href="/?j=${jwt}" class="button">login as guest</a>
            <a class="button disabled">login as admin</a>
        </div>
    </div>
</body>
</html>