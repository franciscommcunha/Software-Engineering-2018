package com.github.adminfaces.starter.infra.security;

import org.omnifaces.util.Faces;
import javax.enterprise.inject.Specializes;
import javax.faces.context.FacesContext;
import javax.inject.Named;
import java.io.IOException;
import java.io.Serializable;
import static com.github.adminfaces.starter.util.Utils.addDetailMessage;
import javax.annotation.PostConstruct;
import javax.enterprise.context.SessionScoped;
import org.omnifaces.cdi.ViewScoped;

/**
 *
 * @author raquelramos
 */

@Named
@ViewScoped
public class CO2Notification implements Serializable {
    
    public static void co2High() throws IOException {
        addDetailMessage("CO2 levels are too <b>high</b>. The windows will be opened.");
        Faces.getExternalContext().getFlash().setKeepMessages(true);
        //Faces.redirect("index.xhtml");
    }
    public static void co2Low() throws IOException {
        addDetailMessage("CO2 levels are too <b>low</b>. The windows will be closed.");
        Faces.getExternalContext().getFlash().setKeepMessages(true);
        //Faces.redirect("index.xhtml");
    }
}

