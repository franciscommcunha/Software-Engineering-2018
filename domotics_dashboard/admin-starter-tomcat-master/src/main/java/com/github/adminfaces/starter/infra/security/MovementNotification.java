package com.github.adminfaces.starter.infra.security;

import org.omnifaces.util.Faces;
import javax.enterprise.inject.Specializes;
import javax.faces.context.FacesContext;
import javax.inject.Named;
import java.io.IOException;
import java.io.Serializable;
import static com.github.adminfaces.starter.util.Utils.addDetailMessage;
import javax.enterprise.context.SessionScoped;
import org.omnifaces.cdi.ViewScoped;

/**
 *
 * @author raquelramos
 */

@Named
@ViewScoped
public class MovementNotification implements Serializable {

    public static void movementDetected() throws IOException {
        addDetailMessage("It was detected movement in the room (name of the room)!");
        Faces.getExternalContext().getFlash().setKeepMessages(true);
        //Faces.redirect("index.xhtml");
    }
}

